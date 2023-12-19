from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

app = Flask(__name__)

app.secret_key = "Secret_key"

# configuring database URI
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:"123Thrissur#"@localhost/crud' 

#DATABSE_URI='mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root', password='', server='localhost', database='crud')
#app.config['SQLALCHEMY_DATABASE_URI'] = DATABSE_URI

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:''@localhost/crud'



# Here, mysql is relational database management software, 
# root is the username, '' is the password as we
# don't have any password, crud is the database name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.app_context().push()

# def test_connection(self):
#     with app.app_context():
#         #test code
#         init_db()

class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))


    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

class Courses(db.Model):
    course_id = db.Column(db.Integer, primary_key = True)
    course = db.Column(db.String(100))
    fees = db.Column(db.String(100))
    teacher = db.Column(db.String(100))


    def __init__(self, course, fees, teacher):
        self.course = course
        self.fees = fees
        self.teacher = teacher


@app.route("/dashboard", methods = ['GET','POST'])
def main():
    student_details = Data.query.all()
    course_details = Courses.query.all()
    #if request.method == 'GET':
    #	return redirect(url_for('index'))
    
    return render_template("main.html", employees = student_details, courses = course_details)
    
@app.route("/student_details")
def Index():
    student_details = Data.query.all()
    return render_template("index.html", employees = student_details)

@app.route('/insert', methods = ['POST'])
def insert():
    if(request.method == 'POST'):
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = Data(name, email, phone)
        db.session.add(my_data)
        db.session.commit()
        
        return redirect(url_for('Index'))
    
@app.route("/update", methods = ['GET', 'POST'])
def update():

    if request.method == "POST":
        my_data = Data.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()

        return redirect(url_for('Index'))
    
@app.route("/delete/<string:id>", methods = ['GET', 'POST'])
def delete(id):
    print(id)
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('Index'))


@app.route("/course_details")
def get_all_courses():
    all_data = Courses.query.all()
    return render_template("courses.html", courses = all_data)

@app.route('/insert_course', methods = ['POST'])
def insert_course():
    if(request.method == 'POST'):
        course = request.form['course']
        fees = request.form['fees']
        teacher = request.form['teacher']

        course_details = Courses(course, fees, teacher)
        db.session.add(course_details)
        db.session.commit()
        
        return redirect(url_for('get_all_courses'))
    

@app.route("/update_course", methods = ['GET', 'POST'])
def update_course():

    if request.method == "POST":
        course_details = Courses.query.get(request.form.get('course_id'))
        print(course_details)
        course_details.course = request.form['course']
        course_details.fees = request.form['fees']
        course_details.teacher = request.form['teacher']

        db.session.commit()

        return redirect(url_for('get_all_courses'))
    
@app.route("/delete_course/<string:id>", methods = ['GET', 'POST'])
def delete_course(id):
    print(id)
    course_details = Courses.query.get(id)
    db.session.delete(course_details)
    db.session.commit()

    return redirect(url_for('get_all_courses'))


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('main'))
    return render_template('login.html', error=error)


if __name__ == "__main__":
    app.run(debug = True)
