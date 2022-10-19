#----------------------------------------------------------------------------#
# Imports.
#----------------------------------------------------------------------------#
import os, csv
from flask import Flask, request, render_template, redirect, url_for, flash, session, send_file, jsonify, abort
from flask_session import Session
from tempfile import mkdtemp
from database.models import db, setup_db, db_drop_and_create_all, User, Enquiry
from auth import login_required
from werkzeug.security import check_password_hash
from datetime import timedelta, date
from Prediction_of_UserInput.prediction_file import Prediction_from_api
from Prediction_from_file.prediction_from_file import Prediction_from_file
from File_operation import file_op
from werkzeug.utils import secure_filename

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)

UPLOAD_FOLDER = os.path.abspath(os.getcwd()) + '/Data/predict'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
setup_db(app)

db_drop_and_create_all()

# use session
@app.before_first_request  # runs before FIRST request (only once)
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)
print(UPLOAD_FOLDER)
#----------------------------------------------------------------------------#
# App Routes.
#----------------------------------------------------------------------------#

# File_prediction route
@app.route('/from_file', methods=['GET','POST'])
@login_required
def from_file():
    if request.method == 'POST':
        try:
            if request.files:
                file = request.files['fromFile']
                file.filename = "prediction_file.csv"
                filepath = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(filepath)
                # read the file
                with open(filepath) as f:
                    csv_file = csv.reader(f)
                    data = [row for row in csv_file]
                    del data[0]
                IDs = [d[0] for d in data]
                pred = Prediction_from_file(filepath)
                predictions = pred.prediction_file_api()
                predictions = [int(p) for p in predictions]

                flash({'type': "success", 'msg': dict(zip(IDs, predictions))})
                response_dic = {}
                response_dic['ids_preds'] = dict(zip(IDs, predictions))

                # return redirect(url_for('prediction_result_file'))
                response_dic['redirect'] = url_for('prediction_result_file')
                return jsonify(response_dic)
        except:
            abort(422)

    user = User.query.filter_by(username=session['user_id']).first()
    user_data = user.details()
    noti = Enquiry.query.filter_by(promoted=False).all()
    numberOfnoti = len(noti)

    return render_template(
        'admin/upload.html',
        current_page="Prediction from file",
        user=user_data, noti=numberOfnoti)

# API route
@app.route('/api', methods=['POST'])
@login_required
def prefict():
    try:
        e_id = int(request.form['e_id'])
        name = request.form['name']
        Int_Learn = float(request.form['int_learn'])
        Fin_Gain = float(request.form['fin_gain'])
        Tech_Cont_Norm = float(request.form['tech_cont_norm'])
        Sys_Int = float(request.form['sys_int'])
        Cod_Test_Task = float(request.form['cod_test_task'])
        Cont_Code_Dec = float(request.form['cont_code_dec'])
        Dec_Right_Del = float(request.form['dec_right_del'])
        Dev_Inv = float(request.form['dev_inv'])
        Proj_Desertion = float(request.form['proj_desertion'])
        Dev_Experience = float(request.form['dev_experience'])
        enquirer = Enquiry.query.get(e_id)
        pred = Prediction_from_api(Int_Learn, Fin_Gain, Tech_Cont_Norm, Sys_Int, Cod_Test_Task, Cont_Code_Dec,Dec_Right_Del, Dev_Inv, Proj_Desertion, Dev_Experience)
        pred_data = pred.prediction_api()

        enquirer.promoted = True
        db.session.commit()
        print(enquirer)
        status = f"Congratulate {name}!! He is Promoted" if pred_data == 1 else f"Sorry {name}!! Not Promoted"
        flash({'type': "success" if pred_data == 1 else "error", 'msg': status})
        return jsonify({
            'Name': name,
            'status': status,
            'redirect': url_for('prediction_result')
        })
    except:
        abort(422)

# Pridiction Result route
@app.route('/prediction_result_file')
@login_required
def prediction_result_file():
    user = User.query.filter_by(username=session['user_id']).first()
    user_data = user.details()
    noti = Enquiry.query.filter_by(promoted=False).all()
    numberOfnoti = len(noti)
    return render_template('admin/prediction_result_file.html', user=user_data, current_page="Prediction Status", noti=numberOfnoti)

# Pridiction Result route
@app.route('/prediction_result')
@login_required
def prediction_result():
    user = User.query.filter_by(username=session['user_id']).first()
    user_data = user.details()
    noti = Enquiry.query.filter_by(promoted=False).all()
    numberOfnoti = len(noti)
    return render_template('admin/prediction_result.html', user=user_data, current_page="Prediction Status", noti=numberOfnoti)

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        email = Enquiry.query.filter_by(email=request.form["email"]).first()
        if email is None:            
            new_enquiry = Enquiry(
                name=request.form["name"],
                education=request.form["education"],
                email=request.form["email"],
                region=request.form["region"],
                fin_gain=request.form["fin_gain"],
                int_learn=request.form["int_learn"],
                dev_inv=request.form["dev_inv"],
                proj_desertion=request.form["proj_desertion"],
                dev_experience=request.form["dev_experience"],
                sys_int=request.form["sys_int"],
                tech_norm=request.form["tech_norm"],
                code_test=request.form["code_test"],
                cont_code_dec=request.form["cont_code_dec"],
                dec_right_del=request.form["dec_right_del"],
                proj_age=request.form["proj_age"],
                date_submitted=date.today()
            )
            db.session.add(new_enquiry)
            db.session.commit()
            # flash({'type': 'success', 'msg': 'You\'ve Successfully submitted your data.'})
            return jsonify({'redirect': 'survey#form', 'success': True})
        else:
            return jsonify({'redirect': 'survey#form', 'success': False})
    return render_template('index.html')

# Survey route
@app.route('/survey', methods=['GET'])
def survey():
    return render_template('survey.html')

#login route
@app.route('/project-leader', methods=['GET', 'POST'])
def login():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    
    # Forget any user_id
    # session.clear()

    if request.method == "POST":
        uname = request.form["username"]
        passw = request.form["password"]

        login = User.query.filter_by(username=uname).first()
        if login is not None:
            # check pass
            if check_password_hash(login.password, passw):
                # Remember which user has logged in
                session["user_id"] = login.username
                flash({'type': 'success', 'msg': f'Welcome back, {login.name}'})
                return redirect(url_for("dashboard"))
        flash({'type': 'error', 'msg': 'Invalid login credentials'})
    return render_template("admin/login.html")


# Dashboard route
@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.filter_by(username=session['user_id']).first()
    user_data = user.details()

    enquiries = Enquiry.query.order_by(db.desc(Enquiry.id)).all()

    noti = Enquiry.query.filter_by(promoted=False).all()
    numberOfnoti = len(noti)

    return render_template(
        'admin/index.html',
        current_page="Dashboard",
        user=user_data,
        enquiries=enquiries,
        noti=numberOfnoti)


# Confirm route
@app.route('/confirm/<int:e_id>')
@login_required
def confirm(e_id):
    user = User.query.filter_by(username=session['user_id']).first()
    user_data = user.details()

    e_query = Enquiry.query.get(e_id)
    noti = Enquiry.query.filter_by(promoted=False).all()
    numberOfnoti = len(noti)

    return render_template(
        'admin/confirm.html',
        current_page="Confirm Data",
        user=user_data, enquiry=e_query.details(), noti=numberOfnoti)

# Prediction result route
@app.route('/status')
@login_required
def status():
    user = User.query.filter_by(username=session['user_id']).first()
    user_data = user.details()
    noti = Enquiry.query.filter_by(promoted=False).all()
    numberOfnoti = len(noti)
    return render_template(
        'admin/prediction_result.html',
        current_page="Prediction Status",
        user=user_data, noti=numberOfnoti)

# Prediction result route
@app.route('/status-file')
@login_required
def status_file():
    user = User.query.filter_by(username=session['user_id']).first()
    user_data = user.details()

    noti = Enquiry.query.filter_by(promoted=False).all()
    numberOfnoti = len(noti)

    return render_template(
        'admin/prediction_result_file.html',
        current_page="File Prediction Status",
        user=user_data, noti=numberOfnoti)


# logout route
@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect('/project-leader')

# logout route
@app.route('/error')
def error():
    return render_template('error.html')

# 404 error handler
@app.errorhandler(404)
def not_found(error):
    return render_template(
        'error.html',
        error_code=404,
        error_msg="The page you are looking for doesn't exist."),404


if __name__ == '__main__':
    app.run(debug=True)