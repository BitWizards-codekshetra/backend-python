from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey , BLOB , DateTime , Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime , timedelta
import json

engine = create_engine('sqlite:///database.db')
Base = declarative_base()

session = sessionmaker()
session.configure(bind=engine)
session = session()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    dob = Column(String, nullable=False)
    password = Column(String(50), nullable=False)
    lat = Column(Float, nullable=False)
    long = Column(Float , nullable=False)
    mobile_number = Column(String(50), nullable=False)
    gender = Column(String(1), nullable=False)
    nationality = Column(String(50), nullable=False)
    profile_pic = Column(String, nullable=False) # BLOB is for storing images

    # def allowed_file(filename):
    #             return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
    #         if product_image and allowed_file(product_image.filename):
    #             image_filename = secure_filename(product_image.filename)
    #             # image_path = os.path.join(app.config['templates/static/'], image_filename)
    #             # print(image_filename, "==========================================")
    #             image_path = os.path.join(app.config['upload_folder'], image_filename)
    #             product_image.save(image_path)
    def __init__(self , name , email , dob , password , lat , long , mobile_number , gender , nationality , profile_pic ):
        self.name = name
        self.email = email
        self.dob = dob
        self.password = password
        self.lat = lat
        self.long = long
        self.mobile_number = mobile_number
        self.gender = gender
        self.nationality = nationality
        self.profile_pic = profile_pic

# user1 = User("user" , "user" , f"datetime.now()" , "user" , 0.0 , 0.0 , "user" , "user" , "user" , '\x30')
# # user2 = User("admin" , "admin" , datetime.now() , "admin" , 0.0 , 0.0 , "admin" , "admin" , "admin" , b'\x30')
# session.add(user1)
# # session.add(user2)
# session.commit()


class Hotel(Base):
    __tablename__ = 'Hotel'
    id = Column(Integer, primary_key=True , autoincrement=True)
    hotel_name = Column(String(50), nullable=False)
    hotel_location = Column(String(50), nullable=False)
    hotel_type = Column(String(50), nullable=False)
    hotel_price = Column(Integer, nullable=False)
    hotel_lat = Column(Float, nullable=False)
    hotel_long = Column(Float, nullable=False)
    # here we would include the dictionary of images like{1 : "image1" , 2 : "image2" , 3 : "image3"}
    hotel_images = Column(String) # BLOB is for storing images
    def set_images(self, images):
        self.hotel_images = json.dumps(images)
    def get_images(self):
        return json.loads(self.hotel_images) 
    is_wifi = Column(Boolean, nullable=False)

    # hotel_image = Column(, nullable=False) # BLOB is for storing images
    def __init__(self , hotel_name , hotel_location , hotel_type , hotel_price , hotel_lat , hotel_long , hotel_images , is_wifi):
        self.hotel_name = hotel_name
        self.hotel_location = hotel_location
        self.hotel_type = hotel_type
        self.hotel_price = hotel_price
        self.hotel_lat = hotel_lat
        self.hotel_long = hotel_long
        self.set_images(hotel_images)
        self.is_wifi = is_wifi


# hotel1 = Hotel("hotel1" , "state1" , "3 star" , 1000 , 0.0 , 0.0 , {1 : "image1" , 2 : "image2" , 3 : "image3"} , True)
# session.add(hotel1)
# session.commit()
        
# class Bookings(Base):
#     __tablename__ = 'Bookings'
#     id = Column(Integer, primary_key=True , autoincrement=True)

# drop table bus , seat 
        

class Bookings(Base):
    __tablename__ = 'Bookings'
    id = Column(Integer, primary_key=True , autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    hotel_id = Column(Integer, ForeignKey('Hotel.id'))
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)
    total_price = Column(Integer, nullable=False)

    user = relationship("User" , backref="Bookings")
    Hotel = relationship("Hotel" , backref="Bookings")

    def __init__(self , user_id , hotel_id , check_in , check_out , total_price):
        self.user_id = user_id
        self.hotel_id = hotel_id
        self.check_in = check_in
        self.check_out = check_out
        self.total_price = total_price

# booking1 = Bookingd(1 , 1 , datetime.now() - timedelta(days=1) , datetime.now()  , 1000)
# session.add(booking1)
# session.commit()
Base.metadata.create_all(engine)
# Base.metadata.drop_all(engine)

# user1 = User("user" , "user" , f"datetime.now()" , "user" , 0.0 , 0.0 , "user" , "user" , "user" , "user.jpg")
# session.add(user1)
# session.commit()