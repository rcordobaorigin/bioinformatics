from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from requester import ObtainIds, GenerateTxt, StringToList, ClustalRequester, ClustalGetResults, ClustalObtainTypeResults, ClustalStatus
import easygui
import webbrowser
import time

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['UPLOAD_FOLDER'] = 'C:/'
 
class DBQuery(Form):
    Database = TextField('Database:', validators=[validators.required()])
    term = TextField('Query: ')
    IdList = TextField('Ids: ')

@app.route("/index.html")
@app.route("/")
def Formatted():
    return render_template("index.html")

@app.route("/Formatted.html", methods=['GET', 'POST'])

def GeneticRequester():
    form = DBQuery(request.form)
    print (form.errors)
    if request.method == 'POST':
            path = easygui.filesavebox(default="genetics.txt")
            if form.validate():
                Ids = ObtainIds(request.form['Database'], request.form['term'])
                GenerateTxt(Ids,request.form['Database'], path)
                flash('Txt Generated in the Path')
            else:
                flash('Error! Database is required')
    return render_template('Formatted.html', form=form)
 
@app.route("/FormDB.html", methods=['GET', 'POST'])

def GeneticId():
    form = DBQuery(request.form)
    print (form.errors)
    if request.method == 'POST':
            patheto = easygui.filesavebox(default="genetics.txt")
            time.sleep(5)
            Ids = StringToList(request.form['IdList'])
            GenerateTxt(Ids,request.form['Database'], patheto)
            flash('Txt Generated in the Path')
    return render_template('FormDB.html', form=form)


@app.route("/ClustalSearch.html", methods=['GET', 'POST'])

def ClustalSearch():
    form = DBQuery(request.form)

    if request.method == 'POST':
        job = ClustalRequester(request.form['email'],request.form['title'],request.form['order'],request.form['dealign'],request.form['mbed'],request.form['mbediteration'],request.form['iterations'],request.form['hmmiterations'],request.form['outfmt'],request.form['path'])
        while (ClustalStatus(job)!='FINISHED'):
            print("Please wait a minute while is calculating")
        typelists = ClustalObtainTypeResults(job)
        ClustalGetResults(job, typelists)
    return render_template("ClustalSearch.html", form=form)

if __name__ == "__main__":
    webbrowser.open_new("http://127.0.0.1:5000/")
    app.run()