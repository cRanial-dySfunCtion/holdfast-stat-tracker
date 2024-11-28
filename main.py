from flask import Flask, render_template, url_for, redirect, request
from backend import *
from test import SimpleForm
import sqlite3
file_check()

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Set a secret key for session management

@app.before_request
def initialize_session():
    pass

@app.route("/", methods=["GET", "POST"])
def home():
    count = row_count_games()
    if request.method == "POST":
        print(request.form)
        if "role" in request.form and "kills" in request.form:
            print("doing something")
            role = request.form["role"]
            kills = request.form["kills"]
            add_game_entry(role, int(kills))
        else:
            return "Missing form data", 400  # Returns an error message to the user
        
        print("updated")
        return render_template('home.html', count=count+1)
    else:
        return render_template('home.html', count=count)

@app.route('/honors', methods=["GET", "POST"])
def honors():
    conn = sqlite3.connect('holdfast.db')  # Replace with your database file
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM honors")
    honors_data = cursor.fetchall()
    conn.close()
    form=SimpleForm()
    if request.method == "POST":
        results = request.form
        print(results)
        return redirect(url_for('home'))
    
    return render_template('honors.html', form=form, honors_data=honors_data)
    

@app.route('/medals')
def medals():
    return render_template('medals.html')

@app.route('/run_reset_database')
def run_reset_database():
    reset_database()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)


