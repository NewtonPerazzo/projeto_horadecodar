# Faz o create do CRUD
from django import forms
from tasks import models


class TaskForm(forms.ModelForm):


    class Meta():
        model = models.Task
        # Campos que quero que apareça no front
        fields = ('title', 'description')