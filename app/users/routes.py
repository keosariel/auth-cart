from flask import (
	request,
	current_app
)
from flask_restful import Resource
from app.utils.functions import JSONResponse
from app.utils.decorators import args_check
from app.validators import LoginValidator, SignupValidator
from app.models import User
from app.error_codes import E101, E102, E103

class Login(Resource):

	@args_check(LoginValidator())
	def post(self, json_data):	
		"""Creates an `access-token` for a user if successfully
		logged in

		JSON parameters:
			:param email: User's email `String` object
			:param password: User's password `String` object

		:return: JSON Object with a token value 

		Reference:
			/auth/validators.py
		"""

		with current_app.app_context():
			email = json_data.email
			password = json_data.password

			# Checks if User with `email` exists
			user = User.query.filter_by(email=email).first()

			if not user:
				return JSONResponse(
					message="User with this email does not exists!", 
					code=E103,
					status=400
				)

			if not user.password_is_valid(password):
				return JSONResponse(
					message="Incorrect username or password!", 
					code=E103,
					status=400
				)

			token = user.generate_token()

			return JSONResponse(data={ 'token' : token, "user": user.to_dict() })

		return JSONResponse(message="Error logging in this account", code=E101, status=500)

class SignUp(Resource):

	@args_check(SignupValidator())
	def post(self, json_data):
		"""Creates an `access-token` for a user if successfully
		signed up

		JSON parameters:
			:param username: User's username `String` object
			:param email: User's email `String` object
			:param password: User's password `String` object

		:return: JSON Object with a token value 

		Reference:
			/auth/validators.py
		"""
		# print(json_data.username, json_data.password)
		with current_app.app_context():
			firstname = json_data.firstname.lower().strip()
			lastname = json_data.lastname.lower().strip()
			username = json_data.username.lower().strip()
			email    = json_data.email.strip()
			password = json_data.password

			# Checks if User with `email` exists
			existing_user = User.query.filter_by(email=email).first()

			if existing_user:
				return JSONResponse(
					message="User with this email already exists!", 
					code=E102,
					status=400
				)

			# Checks if User with `username` exists
			existing_user = User.query.filter_by(username=username).first()

			if existing_user:
				return JSONResponse(
					message="User with this username already exists!", 
					code=E102,
					status=400
				)

			user = User(
       			firstname = firstname,
				lastname = lastname,
				username = username,
				email    = email
			)

			# Hashing password
			user.set_password(password)
			user.save()

			# Setting public ID
			user.set_public_id()
			
			token = user.generate_token()

			return JSONResponse(data={ 'token' : token, "user": user.to_dict() })

		return JSONResponse(message="Error creating an account", code=E101, status=500)