from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import User, Question, Answer

# Create your views here.
def index(request):
	if 'id' not in request.session:
		return redirect(reverse('dashboard:login'))

	data = {
		'questions': Question.objects.all(), 
		'answers': Answer.objects.all(),
		}

	return render(request, 'blackBeltApp/index.html', data)

def login(request):
	if request.method == 'POST':
		return process_login(request)

	return render(request, 'blackBeltApp/login.html')

def process_login(request):
	results = User.objects.UserValidation(request.POST)
	if len(results[0]) < 1:
		request.session['id'] = results[1]
		request.session['username'] = results[2]
		return redirect(reverse('dashboard:index'))

	for error in results:
		messages.error(request, error)
	return redirect(reverse('dashboard:login'))

def logout(request):
	for key in request.session.keys():
		del request.session[key]

	return redirect(reverse('dashboard:login'))

def question(request, id):
	question = Question.objects.get(id=id)

	data = {
		'question': question,
		'answers': Answer.objects.filter(question=question)
	}

	return render(request, 'blackBeltApp/question.html', data)

def newQuestion(request):
	if request.method == 'POST':
		return createNewQuestion(request)

	return render(request, 'blackBeltApp/newQuestion.html')

def createNewQuestion(request):
	results = Question.objects.QuestionValidation(request.POST, request.session['id'])
	if results[1]:
		return redirect(reverse('dashboard:index'))

	for error in results[0]: 
		messages.error(request, error)
	return redirect(reverse('dashboard:newQuestion'))

def editQuestion(request, id):
	if request.method == 'POST':
		return updateQuestion(request, id)

	data = {
		'question': Question.objects.get(id=id),
	}

	return render(request, 'blackBeltApp/editQuestion.html', data)

def updateQuestion(request, id):
	results = Question.objects.editQuestion(request.POST, id, request.session['id'])
	if results[1]:
		return redirect(reverse('dashboard:question', kwargs={'id': id}))
	
	for error in results[0]:
		messages.error(request, error)
	return redirect(reverse('dashboard:editQuestion', kwargs={'id': id}))

def newAnswer(request, id):
	if request.method == 'POST':
		return createNewAnswer(request, id)

	data = {
		'question': Question.objects.get(id=id)
	}

	return render(request, 'blackBeltApp/newAnswer.html', data)

def createNewAnswer(request, id):
	results = Answer.objects.AnswerValidation(request.POST, id, request.session['id'])
	if results[1]:
		return redirect(reverse('dashboard:index'))
		
	for error in results[0]:
		messages.error(request, error)
	return redirect(reverse('dashboard:newAnswer', kwargs={'id': id}))
