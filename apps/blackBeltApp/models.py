from __future__ import unicode_literals
import bcrypt
import re
from datetime import datetime
from django.db import models

#Create your managers here.
class ValidationManager(models.Manager):
	def UserValidation(self, form_info):
		errors = []

		# registration validation
		if 'password2' in form_info:
			EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
			
			firstName = form_info['firstName']
			lastName = form_info['lastName']
			email = form_info['email']
			username = form_info['username']
			dob = form_info['dob']
			password1 = form_info['password1']
			password2 = form_info['password2']

			# name validation
			if len(firstName) < 3:
				errors.append('First Name not valid.')
			if len(lastName) < 3:
				errors.append('Last Name not valid.')

			# password validation
			if password1 != password2:
				errors.append('Passwords do not match.')
			elif len(password1) < 8:
				errors.append('Not a valid password.')

			# email validation
			if len(email) < 1 or not EMAIL_REGEX.match(email):
				errors.append('Not a valid email.')
			elif User.objects.filter(email=email):
				errors.append('Email already in use.')

			# username validation
			if len(username) < 3:
				errors.append('Not a valid username.')
			elif User.objects.filter(username=username):
				errors.append('Username already in use.')

			# dob validation
			if len(str(dob.encode())) < 1:
				errors.append('You forgot to add your date of birth.')
			if dob:
				dob = datetime.strptime(dob, "%Y-%m-%d")
				if dob.date() >= datetime.now().date():
					errors.append('Date of birth is in the future.')

			if len(errors) > 0:
				return (errors)

			password = str(password1)
			hashed = bcrypt.hashpw(password, bcrypt.gensalt())
			User.objects.create(firstName=firstName, lastName=lastName, password=hashed, username=username, email=email, dob=dob)
			user = User.objects.get(username=username)
			return (errors, user.id, user.username)
		else:
		# login validation
			users = User.objects.all()
			print users[0].password
			username = form_info['username'] 
			password = form_info['password'].encode()

			if len(User.objects.filter(username=username)) < 1:
				errors.append('Invalid login information.')
				print "*"*50
				print "invalid login information"
				return (errors)

			user = User.objects.get(username=username)
			hash_entered = bcrypt.hashpw(password, bcrypt.gensalt())

			if username == user.username and bcrypt.hashpw(password, user.password.encode()) == user.password:
				return (errors, user.id, user.username)

			errors.append('Password incorrect.')
			return (errors)

	def QuestionValidation(self, form_info, id):
		errors = []

		question = str(form_info['question'])
		description = str(form_info['description'])

		if len(question) < 8:
			errors.append('Question not long enough.')
		if len(description) < 8:
			errors.append('Description not long enough.')

		if len(errors) > 0:
			return (errors, False)

		user = User.objects.get(id=id)
		Question.objects.create(question=question, description=description, user=user)

		return (errors, True)

	def editQuestion(self, form_info, questionID, userID):
		errors = []
		question = Question.objects.get(id=questionID)
		user = User.objects.get(id=userID)

		if len(form_info['question']) < 8:
			errors.append('Question is not long enough.')
		if len(form_info['description']) < 8:
			errors.append('Description is not long enough.')


		if len(errors) > 0:
			return (errors, False)

		question.question = form_info['question']
		question.description = form_info['description']
		question.save()

		return (errors, True)

	def AnswerValidation(self, form_info, questionID, userID):
		errors = []

		answer = str(form_info['answer'])
		detail = str(form_info['detail'])

		if len(answer) < 8:
			errors.append('Answer is not long enough.')

		if len(errors) > 0:
			return (errors, False)

		user = User.objects.get(id=userID)
		question = Question.objects.get(id=questionID)
		Answer.objects.create(user=user, question=question, answer=answer, detail=detail, like=0)

		return (errors, True)


# Create your models here.
class User(models.Model):
	firstName = models.CharField(max_length=55)
	lastName = models.CharField(max_length=55)
	email = models.CharField(max_length=255)
	username = models.CharField(max_length=55)
	dob = models.DateTimeField()
	password = models.CharField(max_length=55)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = ValidationManager()

class Question(models.Model):
	user = models.ForeignKey('User')
	question = models.CharField(max_length=1000)
	description = models.CharField(max_length=1000)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = ValidationManager()

class Answer(models.Model):
	user = models.ForeignKey('User')
	question = models.ForeignKey('Question')
	answer = models.CharField(max_length=1000)
	detail = models.CharField(max_length=1000, null=True, blank=True)
	like = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = ValidationManager()