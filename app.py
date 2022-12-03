from flask import Flask,request,render_template,redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users,Post,get_name

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
  
@app.route(f'/<int:user_id>')
def show_user(user_id):
    user=Users.query.get_or_404(user_id)
    posts=Post.query.all()
    return render_template('detail.html',user=user,posts=posts)
  
  
@app.route(f'/<int:user_id>/delete',methods=["POST"])
def delete_btn(user_id):
  user=Users.query.get_or_404(user_id)
  db.session.delete(user)
  db.session.commit()
  return redirect('/')



@app.route('/<int:user_id>/edit',methods=["GET"])
def edit_form(user_id):
  
  user=Users.query.get_or_404(user_id)
  return render_template('edit.html',user=user)



@app.route('/<int:user_id>/edit',methods=["POST"])
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


# *****************************************




@app.route('/<int:user_id>/new_post',methods=['GET'])
def new_post(user_id):
  user=Users.query.get_or_404(user_id)
  return render_template('/new_post.html',user=user)

@app.route('/<int:user_id>/new_post',methods=['POST'])
def add_post(user_id):
  
  title=request.form['title']
  content=request.form['content']
  user_id=request.form['user_id']
  
  new_post=Post(title=title,content=content,user_id=user_id)
  db.session.add(new_post)
  db.session.commit()
  
  return redirect(f'/{user_id}')


@app.route('/posts/<int:post_id>')
def detail_post(post_id):
  post=Post.query.get_or_404(post_id)
  
  
  return render_template('post_detail.html',post=post)
  
@app.route('/posts/<int:post_id>/delete',methods=['POST'])
def delete_post(post_id):
  post=Post.query.get_or_404(post_id)
  db.session.delete(post)
  db.session.commit()
  return redirect('/')

@app.route('/posts/<int:post_id>/edit',methods=['GET'])
def edit_post(post_id):
  post=Post.query.get_or_404(post_id)
  return render_template('post_edit.html',post=post)

@app.route('/posts/<int:post_id>/edit',methods=['POST'])
def edit_postBtn(post_id):
  post=Post.query.get_or_404(post_id)
  
  post.title=request.form['title']
  post.content=request.form['content']
  db.session.add(post)
  db.session.commit()
  
  return redirect(f'/posts/{post_id}')

@app.route('/all_posts')
def all_post():
  post=Post.query.all()
  all=Post.query.filter(Post.id >5)

  
 
  
  return render_template('all_posts.html',post=post, all=all)
  
  