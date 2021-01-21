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


@login_required(login_url='/admin')
def search(request):
    if request.method == "POST":
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
        return render(request, 'add_question.html')

@login_required(login_url='/admin')
def save(request):
    if request.method == "POST":
        form = QnaForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'add_question.html', {
                'error_message': 'Both question and answer are required.'
            })
        question = request.POST['question']
        answer = request.POST['answer']
        answer = answer.replace("\r\n", "<br>").replace("\t",'&nbsp;&nbsp;&nbsp;&nbsp;').replace(' ', '&nbsp;')
        q = Question(question_text=question, pub_date=timezone.now())
        q.save()
        q.answer_set.create(answer=answer, approve=0)
        q.save()
        return render(request, 'add_question.html', {
            'success_message': 'Saved done, Thanks'
        })
    else:
        return render(request, 'add_question.html')
    
@login_required(login_url='/admin')
def getDetail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'add_approval.html', {
        'question': question
        })

@login_required(login_url='/admin')
def approve(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_answer = question.answer_set.get(pk=request.POST['answer'])
    except (KeyError, Answer.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'add_approval.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_answer.approve += 1
        selected_answer.save()
        return HttpResponseRedirect(reverse('ask_me:results', args=(question.id,)))

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
def delete(request, question_id):
    Question.objects.filter(pk=question_id).delete()
    return render(request, 'add_question.html', {'success_message': 'Deleted'})
