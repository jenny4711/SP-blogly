from unittest import TestCase
from app import app
from models import db,Users

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly22_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config["TESTING"]=True

app.config["DEBUG_TB_HOSTS"] =["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()

class UsersViewsTestCase(TestCase):
  
  def setUp(self):
    
    Users.query.delete()
    
    user = Users(first_name="TestJenny",last_name="TestLee",image_url="https://e7.pngegg.com/pngimages/643/996/png-clipart-leadership-graphics-computer-icons-illustration-organizational-development-learning.png") 
    db.session.add(user)
    db.session.commit()
    
    self.user_id = user.id
    self.user = user
    
  def tearDown(self):
    db.session.rollback()
    
  def test_home_page(self):
    with app.test_client() as client:
      resp = client.get("/")
      html = resp.get_data(as_text=True)
      
      self.assertEqual(resp.status_code,200)
      self.assertIn("TestJenny",html)
      
  def test_show_user(self):
    with app.test_client() as client:
      resp = client.get(f"/{self.user_id}")
      html = resp.get_data(as_text=True)
      
      self.assertEqual(resp.status_code,200)
      self.assertIn('<h1 id="dt-h1">TESTJENNY TESTLEE</h1>',html)
      self.assertIn(self.user.get_full_name(),html)
      
  def test_new_user(self):
    with app.test_client() as client:
      a ={"first":"TestKyung","last":"shin","img":"https://e7.pngegg.com/pngimages/643/996/png-clipart-leadership-graphics-computer-icons-illustration-organizational-development-learning.png"}          
      resp = client.post("/add_form",data=a,follow_redirects=True)
      html = resp.get_data(as_text=True)
      
      self.assertEqual(resp.status_code,200)
      self.assertIn('<h1 id="dt-h1">TESTKYUNG SHIN</h1>',html)