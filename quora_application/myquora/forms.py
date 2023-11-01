from django import forms
from .models import Questions,Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['text']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']        

