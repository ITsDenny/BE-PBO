from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import bcrypt
import os

app = Flask(__name__)

load_dotenv()

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

MySQL = MySQL(app)

@app.route("/")
def index():
    return "Hello world!"

@app.route("/test_db")
def test_db():
    try:
        cur = MySQL.connection.cursor()
        cur.execute("SELECT 1+1 AS RESULT")
        result = cur.fetchone()
        cur.close()

        return f"OK"
    except Exception as e:
        return f"Eror: {str(e)}"


@app.route("/data")
def data():
    try:
        data = {
            'id' : 1,
            'name' : 'Jonathan Doe',
            'email' : 'John@info.com'
        }

        return jsonify(data)
    except Exception as e:
        return jsonify(e)

def check_password(password,hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def hash_password():
    pass

@app.route("/login", methods=['POST'])
def login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')

        cur = MySQL.connection.cursor()
        cur.execute("SELECT password FROM user WHERE email = %s", (email,))
        user = cur.fetchone()

        if user and check_password(password, user[0]):
            return jsonify({
                'message' : 'Login succeeded',
                'email' : email
            }), 200
        else:
            return jsonify({'message' : 'Email atau password salah!'}), 401

        cur.close()

    except Exception as e:
        return jsonify({'message': 'Error: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
