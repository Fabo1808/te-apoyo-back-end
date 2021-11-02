from enum import unique
from flask_sqlalchemy import SQLAlchemy
from requests.api import delete

db = SQLAlchemy()

class Ong(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ong_name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    location = db.Column(db.String(100), unique= False, nullable= False)
    image= db.Column(db.String(100), unique = False, nullable= False)
    logo = db.Column(db.String(100),unique = False, nullable= False)
    website_address = db.Column(db.String(50),unique= False, nullable =False)
    rif= db.Column(db.String(20),unique= False, nullable = False)
    description= db.Column(db.String(300),unique=False, nullable=True)
    # activities = db.relationship('Activity', backref='org',uselist=True)
    
    def serialize(self):
        return{
            'id':self.id,
            'ong_name':self.ong_name,
            'location': self.location,
            'logo': self.logo,
            'rif': self.rif,
            'website_address':self.website_address,
            # 'activities':[activity.serialize() for activity in self.activities]
        }

    @classmethod
    def create(cls,data_new_ong):
        new_ong= cls(**data_new_ong)
        try:
            db.session.add(new_ong)
            db.session.commit()
            return({"message":"done"})
        except Exception as error:
            db.session.rollback()
            print(error)
            return None

  

# class Favorite(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     url= db.Column(db.String(120),nullable= False)
#     name_favorite= db.Column(db.String(30),nullable= False)
#     user_id= db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#     __table_args__=(db.UniqueConstraint(
#         'user_id',
#         'url',
#         name='unique_fav_for_user'
        
#     ),)

#     def serialize(self):
#         return{
#             'id':self.id,
#             'user_id':self.user_id,
#             'name_favorite': self.name_favorite,
#             'url':self.url,
#         }
    
#     def delete(self):
#         db.session.delete(self)
#         try:
#             db.session.commit()
#             return True
#         except Exception as error:
#             db.session.rollback
#             return None

#     @classmethod
#     def create(cls,data_favorite):
#         new_favorite= cls(**data_favorite)
#         try:
#             db.session.add(new_favorite)
#             db.session.commit()
#             return(new_favorite.serialize())
#         except Exception as error:
#             db.session.rollback()
#             print(error)
#             return None
        