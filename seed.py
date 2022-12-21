from models import db,Users,Post,PostTag,Tag
from app import db,app 

def setup():
  db.drop_all()
  db.create_all()
  
  
  us1=Users(first_name='jenny',last_name='lee',image_url='https://scontent-lga3-1.xx.fbcdn.net/v/t31.18172-8/18556845_10211600352179909_2629863678098565477_o.jpg?stp=c52.0.206.206a_dst-jpg_p206x206&_nc_cat=101&ccb=1-7&_nc_sid=da31f3&_nc_ohc=hXGFIpr-rD8AX_YjvJI&_nc_ht=scontent-lga3-1.xx&oh=00_AfAEclMFyIxJtV6FcfuH5FvYfLD4hdvvPpN_O7CNWl88NA&oe=63C9D5EA')
  us2=Users(first_name='kyung',last_name='kim',image_url='https://scontent-lga3-1.xx.fbcdn.net/v/t31.18172-8/18556845_10211600352179909_2629863678098565477_o.jpg?stp=c52.0.206.206a_dst-jpg_p206x206&_nc_cat=101&ccb=1-7&_nc_sid=da31f3&_nc_ohc=hXGFIpr-rD8AX_YjvJI&_nc_ht=scontent-lga3-1.xx&oh=00_AfAEclMFyIxJtV6FcfuH5FvYfLD4hdvvPpN_O7CNWl88NA&oe=63C9D5EA')
  us=[us1,us2]
  db.session.add_all(us)
  db.session.commit()
  
  ps1=Post(title='hello',content='how r u? ',user_id=1)
  
  db.session.add(ps1)
  db.session.commit()
  
  tg=Tag(name='hey')
  
  db.session.add(tg)
  db.session.commit()
  
  pt=PostTag(post_id=1,tag_id=1)
  
  db.session.add(pt)
  db.session.delete()
  
  
  
  
  
  
  
  



