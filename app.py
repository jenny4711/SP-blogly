from flask import Flask,request,render_template,redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly22'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'chickenzarecod121837'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug =DebugToolbarExtension(app)
app.app_context().push()

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
  users = Users.query.all()
  return render_template('home.html',users=users)

@app.route('/add_form',methods=["GET"])
def get_user():
  return render_template('add_form.html')


@app.route('/add_form', methods=["POST"])
def new_user():
  first=request.form['first']
  last=request.form['last']
  img=request.form['img']
  
  add_user=Users(first_name=first,last_name=last,image_url=img)
  db.session.add(add_user)
  db.session.commit()
  
  return redirect(f'/{add_user.id}')
  
@app.route(f'/<user_id>')
def show_user(user_id):
    user=Users.query.get_or_404(user_id)
    return render_template('detail.html',user=user)
  
@app.route(f'/<user_id>/delete',methods=["POST"])
def delete_btn(user_id):
  user=Users.query.get_or_404(user_id)
  db.session.delete(user)
  db.session.commit()
  return redirect('/')

@app.route('/<user_id>/edit',methods=["GET"])
def edit_form(user_id):
  
  user=Users.query.get_or_404(user_id)
  return render_template('edit.html',user=user)



@app.route('/<user_id>/edit',methods=["POST"])
def edit_btn(user_id):
  user=Users.query.get_or_404(user_id)
  
  user.first_name=request.form['first_name']
  user.last_name=request.form['last_name']
  user.image_url=request.form['img_url']
  print('**********************')
  print(user.first_name)
  print(user.last_name)
  print(user.image_url)
  
  db.session.add(user)
  db.session.commit()
  
  return redirect('/')