from unittest import TestCase

from app import app
from models import db,Users

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly22_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.drop_all()
db.create_all()

class UsersModelTestCase(TestCase):
  
  def setUp(self):
    
    Users.query.delete()
    
  def tearDown(self):
    db.session.rollback()
    
  def test_get_full_name(self):
    user = Users(first_name="TestJenny",last_name="TestLee",image_url="https://e7.pngegg.com/pngimages/643/996/png-clipart-leadership-graphics-computer-icons-illustration-organizational-development-learning.png") 
    self.assertEquals(user.get_full_name(),"TESTJENNY TESTLEE")
    
  
    