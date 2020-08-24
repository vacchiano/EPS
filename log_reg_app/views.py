from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt


# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)

    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    if request.method == 'POST':
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode('utf-8')
        all_users = User.objects.all()
        if all_users == []:
            user_lvl = 9 
        else:
            user_lvl = 1

        new_user = User.objects.create(
            first_name= request.POST['first_name'],
            last_name= request.POST['last_name'],
            email= request.POST['email'],
            password= hashed_pw,
            user_lvl =user_lvl
        )
    return redirect('/')

def login(request):
    if request.method == 'POST':
        all_users = User.objects.all()
        errors = User.objects.login(request.POST)
        username_post = request.POST['username']
        password_post = request.POST['password']
        

        if errors:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/')
        
        else:
            user = User.objects.get(email=username_post)
            request.session['user_id']=user.id
            return redirect('/eps/home')
            

    # return redirect('/')

def users(request):
    context = {
        'users': User.objects.all()
    }

    return render(request, 'all_users.html', context)

def delete(request, user_id):
    d = User.objects.get(id = user_id)
    d.delete()
    return redirect('/users')



def success(request):
    
    if not 'user_id' in request.session:
        return redirect('/')
    else:     
        user = User.objects.get(id=request.session['user_id'])
        all_messages = Message.objects.all()
        all_comments = Comment.objects.all()
        user_id = request.session['user_id']
        context = {
            'user': user,
            'all_messages' : all_messages,
            'all_comments' : all_comments,
            'user_id': user_id
        }
        return render(request, 'success.html', context)
    
def logout(request):
    request.session.clear()
    return redirect('/')

def create_message(request):
    if request.method == 'POST':
        Message.objects.create(
            user = User.objects.get(id=request.session['user_id']),
            message = request.POST['message']
        )

    return redirect('/success')

def create_comment(request, id):
    if request.method == 'POST':

        Comment.objects.create(
            user = User.objects.get(id=request.session['user_id']),
            message = Message.objects.get(id=id),
            content = request.POST['comment']
        )
    return redirect('/success')

def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect('/success')