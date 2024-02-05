# setting up the api's
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from classes import *

class UserAPI(Resource):
    def get(self , email = None , id = None):
        if email:
            user = session.query(User).filter_by(email=email).first()
            if user:
                return {
                    "email" : user.email,
                    "password" : user.password,
                    "mobile_number" : user.mobile_number,
                } , 200
            else:
                return jsonify({"error":"User not found"})
        elif id:
            print(f'id: {id}')
            print(f'type of id: {type(id)}')
            user = session.query(User).filter(User.id==id).first()
            print(user)
            # user = user.first()
            print(user)
            if user:
                return jsonify({
                    "name" : user.name,
                    "email" : user.email,
                    "dob" : user.dob,
                    "lat" : user.lat,
                    "long" : user.long,
                    "mobile_number" : user.mobile_number,
                })
            else:
                return jsonify({"error":"User not found"})
        else:
            return jsonify({"error":"Please provide email or id"})
    
    def post(self):
        data = request.get_json()
        name = data['name']
        email = data['email']
        dob = data['dob']
        password = data['password']
        lat = data['lat']
        long = data['long']
        mobile_number = data['mobile_number']
        gender = data['gender']
        nationality = data['nationality']
        profile_pic = data['profile_pic']
    
        try:
            add_user = User(name , email , dob , password , lat , long , mobile_number , gender , nationality , profile_pic)  
            session.add(add_user)
            session.commit()
        except:
            return jsonify({"error":"User already exists"})
        return jsonify({"success":"User added successfully"})
    
    def put(self , email):
        data = request.get_json()
        name = data['name']
        lat = data['lat']
        long = data['long']
        nationality = data['nationality']
        profile_pic = data['profile_pic']
        user = session.query(User).filter_by(email=email).first()
        if user:
            try:
                user.name = name
                user.lat = lat
                user.long = long
                user.nationality = nationality
                user.profile_pic = profile_pic
                session.commit()
            except:
                return jsonify({"error":"Could not update user"})
            return jsonify({"success":"User updated successfully"})
        else:
            return jsonify({"error":"User not found"})
    # {
    # "name" : "congo",
    # "lat" : "14.56",
    # "long" : "56.14",
    # "nationality" : "Nepalese",
    # "profile_pic" : "me.jpg"
    # }
    # we will use patch request to update only password and mobile_number of the user 
    def patch(self , email):
        data = request.get_json()
        # now we will check if the user has provided password or mobile_number or both
        if 'password' in data:
            password = data['password']
            re_password = data['re_password']
            user = session.query(User).filter_by(email=email).first()
            if user and password == re_password:
                try:
                    user.mobile_number = data['mobile_number']
                    session.commit()
                except:
                    return jsonify({"error":"Could not update the mobile number"})
                return jsonify({"success":"Mobile number updated successfully"})
            else:
                return jsonify({"error":"User not found"})   
        if 'mobile_number' in data:
            mobile_number = data['mobile_number']
            user = session.query(User).filter_by(email=email).first()
            if user and mobile_number==user.mobile_number:
                try:
                    # user.mobile_number = mobile_number
                    user.password = data['new_password']
                    session.commit()
                except:
                    return jsonify({"error":"Could not update the Password"})
                return jsonify({"success":"Password updated successfully"})
            else:
                return jsonify({"error":"User not found"})

    def delete(self , id):
        data = request.get_json()
        password = data['password']
        user = session.query(User).filter_by(id=id).first()
        if user:
            if user.password == password:
                try:
                    session.delete(user)
                    session.commit()
                except:
                    return jsonify({"error":"Could not delete user"})
                return jsonify({"success":"User deleted successfully"})
            else:
                return jsonify({"error":"Incorrect password"})
        else:
            return jsonify({"error":"User not found"})
    


class HotelAPI(Resource):
    def get(self , name = None , id = None):
        if name:
            hotel = session.query(Hotel).filter_by(hotel_name=name).first()
            if hotel:
                return jsonify({
                    "hotel_name" : hotel.hotel_name,
                    "hotel_location" : hotel.hotel_location,
                    "hotel_type" : hotel.hotel_type,
                    "hotel_price" : hotel.hotel_price,
                    "hotel_lat" : hotel.hotel_lat,
                    "hotel_long" : hotel.hotel_long,
                    "hotel_images" : hotel.get_images(),
                    "is_wifi" : hotel.is_wifi
                })
        elif id:
            hotel = session.query(Hotel).filter_by(id=id).first()
            if hotel:
                return jsonify({
                    "hotel_name" : hotel.hotel_name,
                    "hotel_location" : hotel.hotel_location,
                    "hotel_type" : hotel.hotel_type,
                    "hotel_price" : hotel.hotel_price,
                    "hotel_lat" : hotel.hotel_lat,
                    "hotel_long" : hotel.hotel_long,
                    "hotel_images" : hotel.get_images(),
                    "is_wifi" : hotel.is_wifi
                })
            else:
                return jsonify({"error":"No hotel found"})
        else:
            # return all the hotels
            data = request.get_json()
            price = data['price']
            hotels = session.query(Hotel).filter(Hotel.hotel_price <= price).all()
            if hotels:
                hotel_list = []
                for hotel in hotels:
                    hotel_list.append({
                            "hotel_name" : hotel.hotel_name,
                            "hotel_location" : hotel.hotel_location,
                            "hotel_type" : hotel.hotel_type,
                            "hotel_price" : hotel.hotel_price,
                            "hotel_lat" : hotel.hotel_lat,
                            "hotel_long" : hotel.hotel_long,
                            "hotel_images" : hotel.get_images(),
                            "is_wifi" : hotel.is_wifi
                        })
                return jsonify(hotel_list)
    
    def post(self):
        data = request.get_json()
        hotel_name = data['hotel_name']
        hotel_location = data['hotel_location']
        hotel_type = data['hotel_type']
        hotel_price = data['hotel_price']
        hotel_lat = data['hotel_lat']
        hotel_long = data['hotel_long']
        hotel_images = data['hotel_images']
        is_wifi = data['is_wifi']
    
        try:
            add_hotel = Hotel(hotel_name , hotel_location , hotel_type , hotel_price , hotel_lat , hotel_long , hotel_images , is_wifi)  
            session.add(add_hotel)
            session.commit()
        except:
            return jsonify({"error":"Hotel already exists"})
        return jsonify({"success":"Hotel added successfully"})
    
    def put(self , id):
        data = request.get_json()
        hotel_name = data['hotel_name']
        hotel_location = data['hotel_location']
        hotel_type = data['hotel_type']
        hotel_price = data['hotel_price']
        hotel_lat = data['hotel_lat']
        hotel_long = data['hotel_long']
        hotel_images = data['hotel_images']
        is_wifi = data['is_wifi']
        hotel = session.query(Hotel).filter_by(id=id).first()
        if hotel:
            try:
                hotel.hotel_name = hotel_name
                hotel.hotel_location = hotel_location
                hotel.hotel_type = hotel_type
                hotel.hotel_price = hotel_price
                hotel.hotel_lat = hotel_lat
                hotel.hotel_long = hotel_long
                hotel.set_images(hotel_images)
                hotel.is_wifi = is_wifi
                session.commit()
            except:
                return jsonify({"error":"Could not update hotel"})
            return jsonify({"success":"Hotel updated successfully"})
        else:
            return jsonify({"error":"Hotel not found"})
        
    def delete(self , id):
        hotel = session.query(Hotel).filter_by(id=id).first()
        if hotel:
            try:
                session.delete(hotel)
                session.commit()
            except:
                return jsonify({"error":"Could not delete hotel"})
            return jsonify({"success":"Hotel deleted successfully"})
        else:
            return jsonify({"error":"Hotel not found"})
  

class BookingAPI(Resource):
    def get(self , id = None):
        if id:
            booking = session.query(Bookings).filter_by(id=id).first()
            if booking:
                return jsonify({
                    "user_id" : booking.user_id,
                    "hotel_id" : booking.hotel_id,
                    "check_in" : booking.check_in,
                    "check_out" : booking.check_out,
                    "total_price" : booking.total_price
                })
            else:
                return jsonify({"error":"No booking found"})
        else:
            # return all the bookings
            data = request.get_json()
            user_id = data['user_id']
            bookings = session.query(Bookings).filter_by(user_id=user_id).all()
            if bookings:
                booking_list = []
                for booking in bookings:
                    booking_list.append({
                            "user_id" : booking.user_id,
                            "hotel_id" : booking.hotel_id,
                            "check_in" : booking.check_in,
                            "check_out" : booking.check_out,
                            "total_price" : booking.total_price
                        })
                return jsonify(booking_list)
    
    def post(self):
        data = request.get_json()
        user_id = data['user_id']
        hotel_id = data['hotel_id']
        check_in = data['check_in']
        check_in = datetime.strptime(check_in, '%Y-%m-%d')
        check_out = data['check_out']
        check_out = datetime.strptime(check_out, '%Y-%m-%d')
        total_price = data['total_price']

        try:
            add_booking = Bookings(user_id, hotel_id, check_in, check_out, total_price)
            session.add(add_booking)
            session.commit()
        except Exception as e:
            print(e)  # Print the exception traceback
            return jsonify({"error": "Could not add booking"})
        return jsonify({"success": "Booking added successfully"})
    
    def put(self , id):
        data = request.get_json()
        user_id = data['user_id']
        hotel_id = data['hotel_id']
        check_in = data['check_in']
        check_in = datetime.strptime(check_in, '%Y-%m-%d')
        check_out = data['check_out']
        check_out = datetime.strptime(check_out, '%Y-%m-%d')
        total_price = data['total_price']
        booking = session.query(Bookings).filter_by(id=id).first()
        if booking:
            try:
                booking.user_id = user_id
                booking.hotel_id = hotel_id
                booking.check_in = check_in
                booking.check_out = check_out
                booking.total_price = total_price
                session.commit()
            except Exception as e:
                print(e)

                return jsonify({"error":"Could not update booking"})
            return jsonify({"success":"Booking updated successfully"})
        else:
            return jsonify({"error":"Booking not found"})

    def delete(self , id):
        booking = session.query(Bookings).filter_by(id=id).first()
        if booking:
            try:
                session.delete(booking)
                session.commit()
            except:
                return jsonify({"error":"Could not delete booking"})
            return jsonify({"success":"Booking deleted successfully"})
        else:
            return jsonify({"error":"Booking not found"})    
