# app.py

from flask import Flask, request, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)
app.config.from_object('config')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    conn = get_db_connection()
    cursor = conn.execute(f"SELECT * FROM users WHERE name = '{query}'")
    users = cursor.fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in users])

if __name__ == '__main__':
    app.run(debug=True)
