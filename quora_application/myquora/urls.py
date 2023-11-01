from django.urls import path
from .views import login_page, signup_page, logoutview, Homepage, post_question, like_answer,post_answer

urlpatterns = [
    path('', login_page, name='login'),  
    path('logout/', logoutview, name='logout'),  
    path('sign-up/', signup_page, name='signup'), 
    path('homepage', Homepage, name='homepage'), 
    path('post_question/', post_question, name='post_question'),
    path('like_answer/<int:answer_id>/', like_answer, name='like_answer'),
    path('post_answer/<int:question_id>/', post_answer, name='post_answer'),
   
    
]
