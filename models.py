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
    
    
  
    