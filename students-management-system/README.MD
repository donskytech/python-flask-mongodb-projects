# Writeup  
  
# Steps on how to run  
1.  Clone the repository using the below command  
```
git clone https://github.com/donskytech/python-flask-mongodb-projects.git
```  
2. Change into the project directory
```
cd students-management-system
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
6. Run the Flask server with the debug option
```
flask run --debug --host=0.0.0.0
```
7. Open your browser and type the following URL
```
http://<IP>:5000
```
