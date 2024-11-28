from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
import sqlite3


choices_list = [("cpp", "C++"), ("py", "Python"), ("txt", "plain Text"), ("js", "Javascript")]


conn = sqlite3.connect('holdfast.db')
cursor = conn.cursor()
cursor.execute("SELECT honor_ID, name FROM honors WHERE honor_ID NOT IN (SELECT honor_ID FROM earned_honors)")
honors_data = cursor.fetchall()
conn.close()


class SimpleForm(FlaskForm):
    name = StringField("Name")
    submit = SubmitField("Enter")

    language = SelectField(u"Programmng Language", 
    choices=honors_data)