import datetime
from flask_sqlalchemy import SQLAlchemy

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
    
  rep=db.relationship('Users',backref='posts')
  
  def __repr__(self):
    return f"<Post {self.title} {self.content} {self.rep.first_name} {self.rep.get_full_name()} {self.rep.image_url}> "
  

     