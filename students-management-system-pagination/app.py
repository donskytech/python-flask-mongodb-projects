from flask import request,Flask, Response, render_template,redirect,session
from flask_pymongo import PyMongo, ObjectId
import re
from pagination_util import generate_pagination_query
from bson import json_util
import datetime

app = Flask(__name__)
MONGODB_ATLAS_CONN_STRING = "mongodb+srv://iotuser:A7GWhQ3JBYExS8ok@iotdb.e5gtqlx.mongodb.net/studentsdb?retryWrites=true&w=majority"
# LOCAL_MONGODB_CONN = "mongodb://192.168.100.121:27017/studentsdb"
app.config["MONGO_URI"] = MONGODB_ATLAS_CONN_STRING
app.secret_key = 'TEST_KEY'
mongo = PyMongo(app)

limit = 5

@app.route("/")
def home():
    # students = list(mongo.db.students.find({}).sort("last_name", pymongo.ASCENDING))

    query = {}
    sort = ['last_name', 1]

    query, next_key_fn = generate_pagination_query(query, sort)
    students = list(mongo.db.students.find(query).limit(limit).sort([sort]))

    min_key_id = next_key_fn(students, True)
    
    current_page = 0
    session['current_page'] = current_page
    session[f'page_{current_page}'] = {"page_number": 0, 
                       "min_key_id": json_util.dumps(min_key_id),
                       "max_key_id": json_util.dumps(max_key_id)}

    return render_template("/pages/home.html", students=students)

@app.route('/previous-data', methods=['POST'])
def get_previous_rows():
    query = {}
    sort = ['last_name', 1]

    if 'current_page' in session:
        current_page_number = session['current_page']
        print("current page :: " + str(current_page_number))
        
        if 'end_of_rows' in session:
            print("clearing sessions...")
            session.pop('end_of_rows', default=None)
        else:
            current_page_number -= 1
            if current_page_number <= 0:
                current_page_number = 0

    previous_page_info = session[f'page_{current_page_number}']
    print(previous_page_info)
    previous_key = json_util.loads(previous_page_info["min_key_id"])

    query, next_key_fn = generate_pagination_query(query, sort, previous_key, True)
    students = list(mongo.db.students.find(query).limit(limit).sort(([sort])))
    next_key = next_key_fn(students)
    previous_key = next_key_fn(students, True)


    session['current_page'] = current_page_number

    return render_template("/pages/home.html", students=students)

@app.route('/next-data', methods=['POST'])
def get_next_rows():
    query = {}
    sort = ['last_name', 1]
    next_key = None

    if 'current_page' in session:
        current_page_number = session['current_page']
        previous_page_info = session[f'page_{current_page_number}']
        next_key = json_util.loads(previous_page_info["max_key_id"])

    query, next_key_fn = generate_pagination_query(query, sort, next_key)
    students = list(mongo.db.students.find(query).limit(limit).sort([sort]))

    if len(students) == 0:
        session['end_of_rows'] = True
        return render_template("/pages/home.html", students=students)
    
    max_key_id = next_key_fn(students)
    min_key_id = next_key_fn(students, True)

    current_page_number += 1
    current_page = current_page_number
    session['current_page'] = current_page
    session[f'page_{current_page}'] = {"page_number": current_page_number, 
                       "min_key_id": json_util.dumps(min_key_id),
                       "max_key_id": json_util.dumps(max_key_id)}

    return render_template("/pages/home.html", students=students)

@app.route('/edit-student', methods=['GET','POST'])
def edit_student():
    if request.method == "GET":
        student_id = request.args.get('_id')
        student = dict(mongo.db.students.find_one({"_id":ObjectId(student_id)}))

        return render_template('pages/manage-student.html',student=student, 
                               page_title="Edit Student", page_url="edit-student")
    
    elif request.method == "POST":
        _id = request.form['_id']
        student_id = request.form['student_id']
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']

        mongo.db.students.update_one({"_id":ObjectId(_id)},{"$set":{"student_id":student_id,"first_name":first_name
                                                                    ,"middle_name":middle_name,"last_name":last_name }})
        return redirect("/")
    
@app.route('/delete-student', methods=['GET','POST'])
def delete_student():
    if request.method == "GET":
        student_id = request.args.get('_id')
        student = dict(mongo.db.students.find_one({"_id":ObjectId(student_id)}))

        return render_template('pages/manage-student.html',student=student, 
                               page_title="Delete Student", page_url="delete-student", delete="true")
    
    elif request.method == "POST":
        _id = request.form['_id']

        mongo.db.students.delete_one({ "_id": ObjectId(_id)})
        return redirect("/")
    
@app.route('/add-student', methods=['GET','POST'])
def add_student():
    if request.method == "GET":

        return render_template('pages/manage-student.html',
                               page_title="Add Student", page_url="add-student")
    
    elif request.method == "POST":
        student_id = request.form['student_id']
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']

        mongo.db.students.insert_one({"student_id":student_id,
                                      "first_name":first_name,
                                      "middle_name":middle_name,
                                      "last_name":last_name })
        return redirect("/")
    
@app.route('/search-student', methods=['POST'])
def search_student():

    student_id = request.form['student_id']
    last_name = request.form['last_name']

    student_id_regx = re.compile(student_id, re.IGNORECASE)
    last_name_regx = re.compile(last_name, re.IGNORECASE)

    students = list(mongo.db.students.
                    find({"$and":[ {"student_id":student_id_regx}, 
                                  {"last_name":last_name_regx}]}))

    return render_template("/pages/home.html", students=students)

@app.get("/api/validate-student/<student_id>")
def validateStudent(student_id):
    student = list(mongo.db.students.find({"student_id": student_id}))
    
    # Insert Access Logs
    mongo.db.access_logs.insert_one({"student_id": student_id, "date_time": datetime.datetime.utcnow() }) 

    response = Response(
            response=json_util.dumps(student), status=200,  mimetype="application/json")    
    return response