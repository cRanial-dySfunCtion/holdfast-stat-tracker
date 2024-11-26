from flask import Flask, render_template, url_for, redirect, request
from backend import *
file_check()

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Set a secret key for session management

@app.before_request
def initialize_session():
    pass

@app.route("/", methods=["GET", "POST"])
def home():
    count = row_count()
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
        return render_template('home.html', count=count, updated = True)
        
    print("nothing")
    return render_template('home.html', count=count, updated = None)

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/page3')
def page3():
    return render_template('page3.html')

@app.route('/reset_database')
def reset_database():
    reset_database()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)


