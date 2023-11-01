from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from. models import Questions, Answer, Like
from .forms import QuestionForm, AnswerForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# Create your views here.

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            print("Invalid credentials")
    return render(request, 'login.html')


def signup_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username is already taken'})
        
        if not username or not password or not confirm_password:
            return render(request, 'signup.html', {'error': 'All fields are required'})

        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        
        user = User.objects.create_user(username=username, password=password)
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('homepage') 

    return render(request, 'signup.html')

@login_required
def logoutview(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')




@login_required
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user  
            question.save()
            return redirect('homepage')  
    else:
        form = QuestionForm()

    return render(request, 'post_question.html', {'form': form})
@login_required
def Homepage(request):
    quest = Questions.objects.prefetch_related('answer_set').all()
    return render(request,'index.html',{'quest':quest})

@login_required
def like_answer(request, answer_id):
    answer = Answer.objects.get(pk=answer_id)
    existing_like = Like.objects.filter(user=request.user, answer=answer)

    if existing_like.exists():
        existing_like.delete()
    else:
        like = Like(user=request.user, answer=answer)
        like.save()

    like_count = answer.like_set.count()

    return JsonResponse({'like_count': like_count})

def post_answer(request, question_id):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question_id = question_id  
            answer.save()
            return redirect('homepage') 
    else:
        form = AnswerForm()

    return render(request, 'post_answer.html', {'form': form})
