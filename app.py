from flask import Flask,request,render_template,redirect,flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users,Post,get_name,Tag,PostTag
from seed import setup
import os
import re


uri = os.environ.get('DATABASE_URL', 'postgresql:///blogly22')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
print(os.environ)

print('*************************************')
print('*************************************')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','hello1')
print(app.config['SECRET_KEY'])
print('***************')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug =DebugToolbarExtension(app)
app.app_context().push()

connect_db(app)
# db.create_all()

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
  all_tag=Tag.query.all()
  return render_template('/new_post.html',user=user,all_tag=all_tag)

@app.route('/<int:user_id>/new_post',methods=['POST'])
def add_post(user_id):
  
  title=request.form['title']
  content=request.form['content']
  user_id=request.form['user_id']
  check_tag=request.form['check_tag']
  
  new_post=Post(title=title,content=content,user_id=user_id,pt=[PostTag(tag_id=check_tag)])
  db.session.add(new_post)
  db.session.commit()
  
  return redirect(f'/{user_id}')


@app.route('/posts/<int:post_id>')
def detail_post(post_id):
  post=Post.query.get_or_404(post_id)
  # posts=PostTag.query.filter(PostTag.tag_id == tags)
  each_tags=PostTag.query.filter(PostTag.post_id == post_id)
  
  
  return render_template('post_detail.html',post=post,each_tags=each_tags)
  
@app.route('/posts/<int:post_id>/delete',methods=['POST'])
def delete_post(post_id):
  post=Post.query.get_or_404(post_id)
  db.session.delete(post)
  db.session.commit()
  return redirect('/')

@app.route('/posts/<int:post_id>/edit',methods=['GET'])
def edit_post(post_id):
  post=Post.query.get_or_404(post_id)
  each_tags=Tag.query.all()
  return render_template('post_edit.html',post=post,each_tags=each_tags)

@app.route('/posts/<int:post_id>/edit',methods=['POST'])
def edit_postBtn(post_id):
  post=Post.query.get_or_404(post_id)
  
  
  
  post.title=request.form['title']
  post.content=request.form['content']
  pdt_ck=request.form['pdt_ck']
  db.session.add(post)
  db.session.commit()
  
  dupTg=PostTag.query.filter_by(post_id=post_id,tag_id=pdt_ck).first()
  
  if dupTg:
    flash("It already has the Tag!")
    
  else:
    add=PostTag(post_id=post_id,tag_id=pdt_ck)
    db.session.add(add)
    db.session.commit()
    flash("It's a success to add !")
    
  
  
   
  return redirect(f'/posts/{post_id}')

@app.route('/all_posts')
def all_post():
  # post=Post.query.all()
  all=Post.query.order_by(Post.created_at.desc()).limit(5).all()
 
  
  return render_template('all_posts.html', all=all)
# *************************************************************************

@app.route('/tags')
def list_tag():
  tags=Tag.query.all()
  
  return render_template('tags.html',tags=tags)
  
@app.route('/tags/new',methods=['GET'])
def new_tag():
  post=Post.query.all()
  
  return render_template('add_tag.html',post=post)

@app.route('/tags/new',methods=['POST'])
def get_new_tag():
  tag_name=request.form['tg_name']
  check=request.form['check']
  
  
  dup=Tag.query.filter_by(name=tag_name).first()
  
  if dup:
      flash("It's already have the tag!")
      
  else:
      tg= Tag(name=tag_name, pt=[PostTag(post_id=check)])
      db.session.add(tg)
      db.session.commit()
      flash("It's a success to save!")
        
  
  return redirect('/tags')
  

@app.route('/tags/<int:tag_id>',methods=['GET'])
def tag_detail(tag_id):
  tags=Tag.query.get_or_404(tag_id)
  
  
  return render_template('tags_detail.html',tags=tags)


@app.route('/tags/<int:tag_id>/edit',methods=['GET'])
def edit_tag(tag_id):
  tag=Tag.query.get_or_404(tag_id)
  posts=Post.query.all()
  return render_template('edit_tag.html',tag=tag,posts=posts)

@app.route('/tags/<int:tag_id>/edit',methods=['POST'])
def tag_edit(tag_id):
  tag=Tag.query.get_or_404(tag_id)
  tag.name=request.form['tg_name']
  edit_ck=request.form['edit_tg_ck']
  db.session.add(tag)
  db.session.commit()
  
  dupTg=PostTag.query.filter_by(tag_id=tag_id, post_id=edit_ck).first()
  if dupTg:
    flash("It already has the post!")
  else:
    addPt=PostTag(post_id=edit_ck,tag_id=tag_id)
    db.session.add(addPt)
    db.session.commit()
    flash("It's a success to add! ")
      
  return redirect('/tags')
  
  
@app.route('/tags/<int:tag_id>/delete',methods=['POST'])
def delete_tag(tag_id):
  tags=Tag.query.get_or_404(tag_id)
  db.session.delete(tags)
  db.session.commit()
  return redirect('/tags')
  
  
    
# p=Post(title='hihi',content='how r u ?',user_id=1, pt=[PostTag(tag_id=1)])

















# from flask import Flask,request,render_template,redirect,flash
# from flask_debugtoolbar import DebugToolbarExtension
# from models import db, connect_db, Users,Post,get_name,Tag,PostTag
# from seed import setup
# import os
# import re
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] =os.environ.get("DATABASE_URL","postgresql:///blogly22")

# # uri = os.environ.get("DATABASE_URL","postgres://blogly22") x
# # if uri.startswith("postgres://"):x
# #     uri = uri.replace("postgres://", "postgresql:///",1 )x
    



# print('**************os.environ********************')

# print(os.environ)

# print('**************os.environ********************')


# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
# print('**************os.environ********************')

# # app.config['SQLALCHEMY_DATABASE_URI'] = uri
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','hello1')
# print(app.config['SECRET_KEY'])
# print('***************')
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug =DebugToolbarExtension(app)
# app.app_context().push()

# connect_db(app)
# # db.create_all()

# @app.route('/')
# def home_page():
#   users = Users.query.all()
#   return render_template('home.html',users=users)

# @app.route('/add_form',methods=["GET"])
# def get_user():
#   return render_template('add_form.html')


# @app.route('/add_form', methods=["POST"])
# def new_user():
#   first=request.form['first']
#   last=request.form['last']
#   img=request.form['img']
  
#   add_user=Users(first_name=first,last_name=last,image_url=img)
#   db.session.add(add_user)
#   db.session.commit()
  
#   return redirect(f'/{add_user.id}')
  
# @app.route(f'/<int:user_id>')
# def show_user(user_id):
#     user=Users.query.get_or_404(user_id)
#     posts=Post.query.all()
#     return render_template('detail.html',user=user,posts=posts)
  
  
# @app.route(f'/<int:user_id>/delete',methods=["POST"])
# def delete_btn(user_id):
#   user=Users.query.get_or_404(user_id)
#   db.session.delete(user)
#   db.session.commit()
#   return redirect('/')



# @app.route('/<int:user_id>/edit',methods=["GET"])
# def edit_form(user_id):
  
#   user=Users.query.get_or_404(user_id)
#   return render_template('edit.html',user=user)



# @app.route('/<int:user_id>/edit',methods=["POST"])
# def edit_btn(user_id):
#   user=Users.query.get_or_404(user_id)
  
#   user.first_name=request.form['first_name']
#   user.last_name=request.form['last_name']
#   user.image_url=request.form['img_url']
#   print('**********************')
#   print(user.first_name)
#   print(user.last_name)
#   print(user.image_url)
  
#   db.session.add(user)
#   db.session.commit()
  
#   return redirect('/')


# # *****************************************




# @app.route('/<int:user_id>/new_post',methods=['GET'])
# def new_post(user_id):
#   user=Users.query.get_or_404(user_id)
#   all_tag=Tag.query.all()
#   return render_template('/new_post.html',user=user,all_tag=all_tag)

# @app.route('/<int:user_id>/new_post',methods=['POST'])
# def add_post(user_id):
  
#   title=request.form['title']
#   content=request.form['content']
#   user_id=request.form['user_id']
#   check_tag=request.form['check_tag']
  
#   new_post=Post(title=title,content=content,user_id=user_id,pt=[PostTag(tag_id=check_tag)])
#   db.session.add(new_post)
#   db.session.commit()
  
#   return redirect(f'/{user_id}')


# @app.route('/posts/<int:post_id>')
# def detail_post(post_id):
#   post=Post.query.get_or_404(post_id)
#   # posts=PostTag.query.filter(PostTag.tag_id == tags)
#   each_tags=PostTag.query.filter(PostTag.post_id == post_id)
  
  
#   return render_template('post_detail.html',post=post,each_tags=each_tags)
  
# @app.route('/posts/<int:post_id>/delete',methods=['POST'])
# def delete_post(post_id):
#   post=Post.query.get_or_404(post_id)
#   db.session.delete(post)
#   db.session.commit()
#   return redirect('/')

# @app.route('/posts/<int:post_id>/edit',methods=['GET'])
# def edit_post(post_id):
#   post=Post.query.get_or_404(post_id)
#   each_tags=Tag.query.all()
#   return render_template('post_edit.html',post=post,each_tags=each_tags)

# @app.route('/posts/<int:post_id>/edit',methods=['POST'])
# def edit_postBtn(post_id):
#   post=Post.query.get_or_404(post_id)
  
  
  
#   post.title=request.form['title']
#   post.content=request.form['content']
#   pdt_ck=request.form['pdt_ck']
#   db.session.add(post)
#   db.session.commit()
  
#   dupTg=PostTag.query.filter_by(post_id=post_id,tag_id=pdt_ck).first()
  
#   if dupTg:
#     flash("It already has the Tag!")
    
#   else:
#     add=PostTag(post_id=post_id,tag_id=pdt_ck)
#     db.session.add(add)
#     db.session.commit()
#     flash("It's a success to add !")
    
  
  
   
#   return redirect(f'/posts/{post_id}')

# @app.route('/all_posts')
# def all_post():
#   # post=Post.query.all()
#   all=Post.query.order_by(Post.created_at.desc()).limit(5).all()
 
  
#   return render_template('all_posts.html', all=all)
# # *************************************************************************

# @app.route('/tags')
# def list_tag():
#   tags=Tag.query.all()
  
#   return render_template('tags.html',tags=tags)
  
# @app.route('/tags/new',methods=['GET'])
# def new_tag():
#   post=Post.query.all()
  
#   return render_template('add_tag.html',post=post)

# @app.route('/tags/new',methods=['POST'])
# def get_new_tag():
#   tag_name=request.form['tg_name']
#   check=request.form['check']
  
  
#   dup=Tag.query.filter_by(name=tag_name).first()
  
#   if dup:
#       flash("It's already have the tag!")
      
#   else:
#       tg= Tag(name=tag_name, pt=[PostTag(post_id=check)])
#       db.session.add(tg)
#       db.session.commit()
#       flash("It's a success to save!")
        
  
#   return redirect('/tags')
  

# @app.route('/tags/<int:tag_id>',methods=['GET'])
# def tag_detail(tag_id):
#   tags=Tag.query.get_or_404(tag_id)
  
  
#   return render_template('tags_detail.html',tags=tags)


# @app.route('/tags/<int:tag_id>/edit',methods=['GET'])
# def edit_tag(tag_id):
#   tag=Tag.query.get_or_404(tag_id)
#   posts=Post.query.all()
#   return render_template('edit_tag.html',tag=tag,posts=posts)

# @app.route('/tags/<int:tag_id>/edit',methods=['POST'])
# def tag_edit(tag_id):
#   tag=Tag.query.get_or_404(tag_id)
#   tag.name=request.form['tg_name']
#   edit_ck=request.form['edit_tg_ck']
#   db.session.add(tag)
#   db.session.commit()
  
#   dupTg=PostTag.query.filter_by(tag_id=tag_id, post_id=edit_ck).first()
#   if dupTg:
#     flash("It already has the post!")
#   else:
#     addPt=PostTag(post_id=edit_ck,tag_id=tag_id)
#     db.session.add(addPt)
#     db.session.commit()
#     flash("It's a success to add! ")
      
#   return redirect('/tags')
  
  
# @app.route('/tags/<int:tag_id>/delete',methods=['POST'])
# def delete_tag(tag_id):
#   tags=Tag.query.get_or_404(tag_id)
#   db.session.delete(tags)
#   db.session.commit()
#   return redirect('/tags')
  
  
    
# # p=Post(title='hihi',content='how r u ?',user_id=1, pt=[PostTag(tag_id=1)])