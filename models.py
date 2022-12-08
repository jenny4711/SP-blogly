import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc


db =SQLAlchemy()

url= "https://e7.pngegg.com/pngimages/643/996/png-clipart-leadership-graphics-computer-icons-illustration-organizational-development-learning.png"

def connect_db(app):
  db.app=app
  db.init_app(app)
  
class Users(db.Model):
  __tablename__='users'
  
  id = db.Column(db.Integer,
                primary_key=True,
                autoincrement=True)
      
  first_name= db.Column(db.Text,
                      nullable=False,
                      unique=True)
      
  last_name= db.Column(db.Text,
                      nullable=False,)
  
  image_url= db.Column(db.Text,
                      nullable=False,
                      default=url )
  reps=db.relationship('Post',cascade='all, delete-orphan')
  
  def get_full_name(self):
    first=self.first_name
    last=self.last_name
    upper= first.upper()
    up=last.upper()
    return f'{upper} {up}'
  
  def __repr__(self):
    return f"<Users {self.first_name} {self.get_full_name()} {self.image_url} >"
  

class Post(db.Model):
  __tablename__ = 'posts'
  
  id = db.Column(db.Integer,
                 primary_key=True,
                 autoincrement=True)
  
  title = db.Column(db.Text,
                    nullable=False,)
  
  content = db.Column(db.Text,
                      nullable=False)
  
  created_at = db.Column(db.DateTime,
                         nullable=False,
                         default=datetime.datetime.now)  
  
  user_id= db.Column(db.Integer,
                     db.ForeignKey('users.id'))
    
  rep=db.relationship('Users')
  pt=db.relationship('PostTag',backref='pt',cascade='all, delete-orphan')
  
  
 
   
  
  
 
    
  
  def __repr__(self):
    return f"<Post {self.title} {self.content} > "
  
def get_name():
  pt = Post.query.all()
  
  for p in pt:
    if p.rep is not None:
      print(p.title,p.id,p.rep.id,p.rep.first_name)
      
    else:
      print(p.title) 

class Tag(db.Model):
  
  
  __tablename__='tags'
  
  id = db.Column(db.Integer,
                primary_key=True,
                autoincrement=True)       
  
  name = db.Column(db.Text,
                nullable=False,
                unique=True)
  
  
  pt=db.relationship('PostTag',backref='tg',cascade='all, delete-orphan')
  postTg=db.relationship('Post',
                        secondary="post_tags",
                        backref="tg")
 
    
class PostTag(db.Model):
  
  __tablename__='post_tags'
  
  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
  
  tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)  
  
   
   
   
   
     