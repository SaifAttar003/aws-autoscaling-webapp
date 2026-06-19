from flask import Flask, jsonify
import mysql.connector
import os
import time

app = Flask(__name__)

def get_connection():
    while True:
        try:
            conn = mysql.connector.connect(
                host=os.environ['DB_HOST'],
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASSWORD'],
                database=os.environ['DB_NAME']
            )
            return conn
        except Exception as e:
            print("Waiting for DB...", e)
            time.sleep(5)

@app.route('/')
def home():
    return "App is running!"

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/db-test')
def db_test():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50))")
    cursor.execute("INSERT INTO users(name) VALUES('Saif')")
    conn.commit()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    return jsonify({"users": str(rows)}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)