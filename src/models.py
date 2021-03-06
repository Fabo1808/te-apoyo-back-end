from enum import unique
from flask_sqlalchemy import SQLAlchemy
from requests.api import delete

db = SQLAlchemy()

class Ong(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ong_name = db.Column(db.String(20),  unique=True, nullable=False)
    password = db.Column(db.String(20),  unique=False, nullable=False)
    location = db.Column(db.String(100), unique= False, nullable= False)
    image= db.Column(db.String(100), unique = False, nullable= False)
    logo = db.Column(db.String(100),unique = True, nullable= False)
    website_address = db.Column(db.String(50),unique= True, nullable =False)
    rif= db.Column(db.String(100),unique= True, nullable = False)
    bank= db.Column(db.String(100), unique=False, nullable= False)
    account= db.Column(db.String(100), unique= False,nullable=False)
    description= db.Column(db.String(300),unique=False, nullable=True)
    activities = db.relationship('Activity', backref='ong',uselist=True)
   
    
    def serialize(self):
        return{
            'id':self.id,
            'ong_name':self.ong_name,
            'location': self.location,
            'logo': self.logo,
            'image':self.image,
            'rif': self.rif,
            'website_address':self.website_address,
            'description':self.description,
            'bank':self.bank,
            'account':self.account,
            'activities':[activity.serialize() for activity in self.activities]
        }

    @classmethod
    def create(cls,data_new_ong):
        new_ong= cls(**data_new_ong)
        try:
            db.session.add(new_ong)
            db.session.commit()
            return(new_ong.serialize())
        except Exception as error:
            db.session.rollback()
            print(error)
            return None




class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_name = db.Column(db.String(20), unique=False, nullable=False)
    image= db.Column(db.String(100), unique = False, nullable= False)
    description= db.Column(db.String(300),unique=False, nullable=False)
    quota = db.Column(db.Integer, unique = False, nullable = False)
    date= db.Column(db.String(50),unique=False, nullable= False)
    ong_id = db.Column(db.Integer, db.ForeignKey("ong.id"), nullable=False)
    volunteers = db.relationship('Voluntary', backref='activity',uselist=True)
    __table_args__=(db.UniqueConstraint(
        'ong_id',
        'date',
        name='unique_activity_for_date'
        
    ),)
    
    def serialize(self):
        return{
            'id':self.id,
            'activity_name':self.activity_name,
            'image': self.image,
            'description': self.description,
            'date': self.date,
            'ong_id':self.ong_id,
            'quota':self.quota,
            'volunteers':[voluntary.serialize() for voluntary in self.volunteers]
        }
    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback
            return None

    @classmethod
    def create(cls,data_new_activity):
        new_activity= cls(**data_new_activity)
        try:
            db.session.add(new_activity)
            db.session.commit()
            return(new_activity.serialize())
        except Exception as error:
            db.session.rollback()
            print(error)
            return None

  



class Voluntary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    lastName= db.Column(db.String(20), unique = False, nullable= False)
    email = db.Column(db.String(50),unique=False, nullable=False)
    phone= db.Column(db.String(15), unique = False, nullable = False)
    activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"), nullable=False)
    __table_args__=(db.UniqueConstraint(
        'name',
        'lastName',
        'phone',
        'activity_id',
        name='unique_voluntary_for_activity'
        
    ),)

    
    def serialize(self):
        return{
            'id':self.id,
            'name':self.name,
            'lastName': self.lastName,
            'email': self.email,
            'phone': self.phone,
            'activity_id':self.activity_id
        }


    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback
            return None

    @classmethod
    def create(cls,data_new_voluntary):
        new_voluntary= cls(**data_new_voluntary)
        try:
            db.session.add(new_voluntary)
            db.session.commit()
            return({"message":"done"})
        except Exception as error:
            db.session.rollback()
            print(error)
            return None

  

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30),unique=False,nullable= False)
    lastName = db.Column(db.String(30),unique=False,nullable= False)
    phone= db.Column(db.String(30),unique=False,nullable= False)
    email = db.Column(db.String(30),unique=False,nullable= False)
    message = db.Column(db.String(30),unique=False,nullable= False)
    date = db.Column(db.String(30),unique=False,nullable= False)


    def serialize(self):
        return{
        'id':self.id,
        'name': self.name,
        'lastName':self.lastName,
        'massage':self.message,
        'email':self.email,
        'phone':self.phone
        }
 

    @classmethod
    def create(cls,data):
        new_message= cls(**data)
        try:
            db.session.add(new_message)
            db.session.commit()
            return({"message":"Mensaje Enviado"})
        except Exception as error:
            db.session.rollback()
            print(error)
            return None
        