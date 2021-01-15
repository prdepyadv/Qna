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

def save(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    if request.method == "POST":
        form = QnaForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'add_question.html', {
                'latest_question_list': latest_question_list,
                'error_message': 'Both question and answer are required.'
            })
        question = request.POST['question']
        answer = request.POST['answer']
        q = Question(question_text=question, pub_date=timezone.now())
        q.save()
        q.answer_set.create(answer=answer, approve=0)
        q.save()
        return render(request, 'add_question.html', {
            'latest_question_list': latest_question_list,
            'success_message': 'Saved done, Thanks'
        })
    else:
        return render(request, 'add_question.html', {'latest_question_list': latest_question_list})


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    if request.method == "POST":
        question = Question.objects.filter(question_text__contains=request.POST['search'])
        if not question:
            return render(request, 'add_question.html', {
                'latest_question_list': latest_question_list,
                'question': question,
                'error_message': "Sorry, nothing really found"
            })
        else:
            question = question.last()
        return render(request, 'results.html', {
            'latest_question_list': latest_question_list,
            'question': question
        })
    else :
        return render(request, 'add_question.html', {'latest_question_list': latest_question_list})
    

def getDetail(request, question_id):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'detail.html', {
        'latest_question_list': latest_question_list,
        'question': question
        })

def approve(request, question_id):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_answer = question.answer_set.get(pk=request.POST['answer'])
    except (KeyError, Answer.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'detail.html', {
            'latest_question_list': latest_question_list,
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_answer.approve += 1
        selected_answer.save()
        return HttpResponseRedirect(reverse('ask_me:results', args=(question.id,)))


def results(request, question_id):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {
        'latest_question_list': latest_question_list,
        'question': question
        })
