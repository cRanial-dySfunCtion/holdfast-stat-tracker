from flask import Flask, render_template, url_for, redirect, request
from backend import *
file_check()

app = Flask(__name__)
app.secret_key = 'supersecretkey'




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
            return "Missing form data", 400
        
        print("updated")
        return render_template('home.html', count=count+1)
    else:
        return render_template('home.html', count=count)




@app.route('/honors', methods=["GET", "POST"])
def honors():
    all_honors_data = get_all_honors()
    earned_honors = get_earned_honors()
    form=honorSelectField()
    form.honor_ID.choices=select_field_honor_data()
    if request.method == "POST":
        results = request.form
        add_honor(results["honor_ID"])
        return redirect(url_for('home'))
    return render_template('honors.html', form=form, honors_data=all_honors_data, earned_honors=earned_honors)
    

@app.route('/medals', methods=["GET", "POST"])
def medals():
    all_medals_data = get_all_medals()
    earned_medals = get_earned_medals()
    form=medalSelectField()
    form.medal_ID.choices=select_field_medal_data()
    if request.method == "POST":
        results = request.form
        add_medal(results["medal_ID"])
        return redirect(url_for('home'))
    return render_template('medals.html', form=form, medals_data=all_medals_data, earned_medals=earned_medals)

@app.route('/run_reset_database')
def run_reset_database():
    reset_database()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)


