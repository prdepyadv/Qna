from django import http
from django.contrib.auth.decorators import login_required
from django.db.models import query
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from .models import Answer, Question
from django.http import Http404
from django.urls import reverse
from django.utils import timezone
from .form import QnaForm
from django.http.response import JsonResponse
from functools import reduce
import operator
from PyDictionary import PyDictionary
import requests
from django.utils.html import strip_tags
from decouple import config
from django.core.mail import send_mail
from .library.emailer import emailer


@login_required(login_url='/admin')
def search(request):
    if request.method == "GET":
        return render(request, 'add_question.html')
    elif request.method == "POST":
        searchText = request.POST['search'].strip()
        if not searchText:
            return render(request, 'add_question.html')
        searchTextList = searchText.split(' ')
        searchTextList.append(searchText)
        questions = reduce(operator.or_, (
            Question.objects.filter(question_text__icontains=text)
            for text in searchTextList))
        if questions:
            return render(request, 'search.html', {
                'questions': questions,
                'search_message': searchText
            })

        """ Try Again - Synonym Game """
        searchTextList = searchText.split(' ')
        newSearchList = []
        for search in searchTextList:
            dictionary = PyDictionary()
            searchList = dictionary.synonym(search)
            if searchList:
                newSearchList.append(search)
                newSearchList += searchList
        if newSearchList:
            questions = reduce(operator.or_, (
                Question.objects.filter(
                    question_text__icontains=text)
                for text in newSearchList))
            if questions:
                return render(request, 'search.html', {
                    'questions': questions,
                    'search_message': searchText
                })

        return render(request, 'add_question.html', {
            'error_message': "Sorry, nothing really found",
            'search_message': searchText
        })
    else:
        return JsonResponse({'error': True, 'message': 'Invalid request'})

@login_required(login_url='/admin')
def index(request):
    if request.method == 'GET':
        return render(request, 'add_question.html')
    elif request.method == "POST":
        form = QnaForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'add_question.html', {
                'error_message': 'Both question and answer are required.'
            })
        question = request.POST['question']
        answer = request.POST['answer']
        question = question.strip()
        answer = answer.strip()
        answer = answer.replace("\r\n", "<br>").replace("\t",'&nbsp;&nbsp;&nbsp;&nbsp;').replace(' ', '&nbsp;')

        exists = True
        try:
            searchAns = Question.objects.get(
                question_text__iexact=question)
        except Question.DoesNotExist:
            exists = False
        except Question.MultipleObjectsReturned:
            exists = True
        except Exception as e:
            print(e)
            return render(request, 'add_question.html', {
                'error_message': 'Oops! Something went wrong'
            })
        if exists:
            return render(request, 'add_question.html', {
                'error_message': 'Duplicate question.'
            })

        q = Question(question_text=question, pub_date=timezone.now())
        q.save()
        q.answer_set.create(answer=answer)
        q.save()

        message = "Hello Team,\nThis new question '" + \
            strip_tags(
                question) + "' just has been added on server.\nKindly look into it.\n\nThanks :)"
        try:
            mailer = emailer()
            mailer.emailQuestion('New Question added!!', message)
        except Exception as e:
            print(e)
        
        return render(request, 'add_question.html', {
            'success_message': 'Saved done, Thanks'
        })
        
    else:
        return JsonResponse({'error': True, 'message': 'Invalid request'})
    
@login_required(login_url='/admin')
def getDetail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'add_approval.html', {
        'question': question
        })

@login_required(login_url='/admin')
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {
        'question': question
        })

@login_required(login_url='/admin')
def lastestQuestions(request):
    if request.method == 'GET':
        latest_question_list = Question.objects.order_by('-pub_date')[:10]
        if not latest_question_list:
            return JsonResponse({'success': False, 'latest_question_list': {}, 'message': 'No questions are available.'})
        list = {}
        for question in latest_question_list:
            list[question.id] = question.question_text
        return JsonResponse({'success': True,'latest_question_list':list, 'message':'Latest 10 questions'})

@login_required(login_url='/admin')
def deleteQuestion(request, question_id):
    Question.objects.filter(pk=question_id).delete()
    return render(request, 'add_question.html', {'success_message': 'Deleted successfully.'})

@login_required(login_url="/admin")
def updateAnswer(request):
    answer = request.POST['answer']
    answer_id = request.POST['id']

    answer = answer.strip()
    if not answer or not answer_id:
        return JsonResponse({'error': True, 'message': 'Answer cannot be empty'})

    answer = answer.replace("\r\n", "<br>").replace(
    "\t", '&nbsp;&nbsp;&nbsp;&nbsp;').replace(' ', '&nbsp;')
    answerDataFromDb = get_object_or_404(Answer, id=answer_id)
    if answerDataFromDb.answer.lower() == answer.lower():
        return JsonResponse({'error': True, 'message': 'Duplicate data'})

    answerDataFromDb.answer = answer
    answerDataFromDb.save()
    return JsonResponse({'error': False, 'message': 'Saved'})

@login_required(login_url="/admin")
def deleteAnswer(request):
    answer_id = request.POST['id']
    if not answer_id:
        return JsonResponse({'error': True, 'message': 'Answer Id cannot be empty'})

    Answer.objects.filter(id=answer_id).delete()
    return JsonResponse({'error': False, 'message': 'Deleted'})

@login_required(login_url="/admin")
def saveAnswer(request):
    answer = request.POST['answer']
    questionId = request.POST['questionId']

    answer = answer.strip()
    if not answer or not questionId:
        return JsonResponse({'error': True, 'message': 'Answer cannot be empty'})

    answer = answer.replace("\r\n", "<br>").replace(
        "\t", '&nbsp;&nbsp;&nbsp;&nbsp;').replace(' ', '&nbsp;')
    questionDataFromDb = get_object_or_404(Question, pk=questionId)
    
    exists = True
    try:
        searchAns = questionDataFromDb.answer_set.get(
            answer__iexact=answer)
    except Answer.DoesNotExist:
        exists = False
    except Question.MultipleObjectsReturned:
        exists = True
    except Exception as e:
        print(e)
        return JsonResponse({'error': True, 'message': 'Oops! Something went wrong'})

    if exists:
        return JsonResponse({'error': True, 'message': 'Duplicate answer.'})
    
    questionDataFromDb.answer_set.create(answer=answer)
    questionDataFromDb.save()

    message = "Hello Team,\nNew Answer for Question '" + \
    strip_tags(
        questionDataFromDb.question_text) + "' just has been added on server.\nKindly look into it.\n\nThanks :)"
    try:
        mailer = emailer()
        mailer.emailQuestion('New Answer added!!', message)
    except Exception as e:
        print(e)

    return JsonResponse({'error': False, 'message': 'Saved'})

@login_required(login_url='/admin')
def addLike(request, answer_id):
    if not answer_id:
        return JsonResponse({'error': True, 'message': 'Answer Id cannot be empty'})

    answerDataFromDb = get_object_or_404(Answer, id=answer_id)
    answerDataFromDb.approve += 1
    answerDataFromDb.save()
    return JsonResponse({'error': False, 'message': 'Done', 'data': answerDataFromDb.approve})

@login_required(login_url='/admin')
def addDislike(request, answer_id):
    if not answer_id:
        return JsonResponse({'error': True, 'message': 'Answer cannot be empty'})

    answerDataFromDb = get_object_or_404(Answer, id=answer_id)
    answerDataFromDb.disapprove += 1
    answerDataFromDb.save()
    return JsonResponse({'error': False, 'message': 'Done', 'data': answerDataFromDb.disapprove})
