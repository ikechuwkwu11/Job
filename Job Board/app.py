from flask import Flask,jsonify,request
from models import User,Job,Application,db
from flask_login import login_user,logout_user,login_required,current_user,LoginManager
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_board.db'
app.config['SECRET_KEY'] = ''

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register/',methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        if not username or not password or not role:
            return jsonify({'message':'Username and password are required'}),404

        hashed_pw = generate_password_hash(data['password'])
        new_user = User(username=username,password=hashed_pw,role=role)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message':'You have successfully been registered'}),201
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@app.route('/login/',methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'message':'Wrong details pls try again'})

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return jsonify({'message':'You have been logged in'}),200
        return jsonify({'message':'Invalid details.. Please try again'}),404
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@app.route('/logout/',methods=['GET'])
@login_required
def logout():
    try:
        logout_user()
        return jsonify({'message':'You have been logged out successfully'}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@app.route('/job/',methods=['POST'])
@login_required
def job():
    try:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        location = data.get('location')
        company = data.get('company')
        if not title or not description or not location or not company:
            return jsonify({'message':'Please fill in all information'}),404

        if current_user.role != 'employer':
            return jsonify({'error':'Only employers can post jobs'}),404

        user = Job(title = title,description = description, location = location, company = company)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message':'Your job has been posted!'}),201
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@app.route('/get_job/',methods = ['GET'])
@login_required
def get_job():
    try:
        jobs = Job.query.all()
        job_list = [
            {
                "title":job.title,
                "description":job.description,
                "location":job.location,
                "company":job.company,
                "user_id":job.user_id
            }
            for job in jobs
        ]
        return jsonify(job_list),200
    except Exception as e:
        return jsonify({'message':'Internal server error',"error":str(e)}),500

@app.route('/single_job/<int:job_id>',methods=['GET'])
@login_required
def single_job(job_id):
    try:
        job = Job.query.get(job_id)
        if not job:
            return jsonify({'message':'Job not found'})

        job_data = {
            "id":job.id,
            "title":job.title,
            "description":job.description,
            "location":job.location,
            "company":job.company,
            "user_id":job.user_id
        }
        return jsonify({'single_job':job_data}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@app.route('/delete_job/<int:job_id>',methods=['DELETE'])
@login_required
def delete_job(job_id):
    try:
        job = Job.query.get(job_id)
        db.session.delete(job)
        db.session.commit()
        return jsonify({'message':'You have deleted this job offer'}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@app.route('/application/',methods=['POST'])
@login_required
def application():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        job_id = data.get('job_id')
        status = data.get('status')
        if not user_id or not job_id or not status:
            return jsonify({'message':'Please put in the correct details'}),404

        application = Application(user_id=user_id,job_id=job_id,status=status)
        db.session.add(application)
        db.session.commit()
        return jsonify({'message':'Your application has been applied'}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@app.route('/get_application/',methods=['GET'])
@login_required
def get_application():
    try:
        applications = Application.query.all()
        application_list = [
            {
                "user_id": application.user_id,
                "job_id": application.job_id,
                "status":application.status
            }
            for application in applications
        ]
        return jsonify(application_list),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@app.route('/single_application/<int:application_id>',methods=['GET'])
@login_required
def single_application(application_id):
    try:
        application = Application.query.get(application_id)
        if not application:
            return jsonify({'message':'application not found'})


        application_list = {
            "user_id":application.user_id,
            "job_id":application.job_id,
            "status":application.status
        }
        return jsonify({'application_data':application_list}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@app.route('/delete_application/<int:application_id>',methods=['DELETE'])
@login_required
def delete_application(application_id):
    try:
        application = Application.query.get(application_id)
        db.session.delete(application)
        return jsonify({'message':'You application has been deleted'}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
