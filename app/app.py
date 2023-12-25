from flask import Flask,jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  
app.config['MYSQL_DB'] = 'pbo_db'

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


if __name__ == '__main__':
    app.run(debug=True)
