from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('users', views.users),
    path('<int:user_id>/delete', views.delete),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),
    path('create_message', views.create_message),
    path('create_comment/<int:id>', views.create_comment),
    path('delete_comment/<int:comment_id>', views.delete_comment)
]