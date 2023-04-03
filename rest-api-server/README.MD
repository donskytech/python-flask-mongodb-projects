
# Writeup  
https://www.donskytech.com/create-a-rest-api-server-with-python-flask-and-mongodb/  
  
![Featured Image - Python Flask MongoDB REST API Server](https://user-images.githubusercontent.com/69466026/229530573-a7762815-af49-4c99-86e1-c46cb20ace00.jpg)
# Prerequisites  
1.  Create a MongoDB Atlas cluster.
2.  Create a database called sensors_db with a collection sensors  
  
# Steps on how to run  
1.  Clone the repository using the below command  
```
git clone https://github.com/donskytech/python-flask-mongodb-projects.git
```  
2. Change into the project directory
```
cd rest-api-server
```
3. Open the project in Visual Studio Code and then open a new terminal.  Create a virtual environment using the below command
```
# Windows
py -m venv .venv
# Linux
python -m venv .venv
```
4. Activate the virtual environment
```
# Windows
.\.venv\Scripts\activate
# Linux
source .venv\bin\activate
```
5. Install the dependencies
```
pip install -r requirements.txt
```  
6. Rename the .env.local to .env
```
mv .env.local .env
```  
7. Replace the value of the .env file to your MongoDB Atlas  
```
MONGO_DB_CONN_STRING=mongodb+srv://<DB_USER_NAME>:<DB_PASSWORD>@<MONGO_DB_ATLAS_ENDPOINT>/sensors_db
```
8. Run the Flask server
```
flask run
```
9. Open your browser and type the following URL
```
http://<IP>:5000
```
