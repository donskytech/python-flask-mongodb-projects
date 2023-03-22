from flask import request,Flask,render_template,redirect
from flask_pymongo import PyMongo, ObjectId
import pymongo
import re

app = Flask(__name__)
MONGODB_ATLAS_CONN_STRING = "mongodb+srv://iotuser:A7GWhQ3JBYExS8ok@iotdb.e5gtqlx.mongodb.net/studentsdb?retryWrites=true&w=majority"
# LOCAL_MONGODB_CONN = "mongodb://192.168.100.121:27017/studentsdb"
app.config["MONGO_URI"] = MONGODB_ATLAS_CONN_STRING
mongo = PyMongo(app)

@app.route("/")
def home():
    students = list(mongo.db.students.find({}).sort("last_name", pymongo.ASCENDING))

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