from django.forms import ModelForm, URLInput
from .models import Project
from django.forms import ClearableFileInput, ModelForm, TextInput, Textarea

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = [ 'user_project','ratings', 'updated', 'created']
        widgets = {
            'title' :  TextInput(attrs={'class':'post-form-title'}),
            'image' :  ClearableFileInput (attrs={'class':'post-form-image'}),
            'description' : Textarea(attrs={'class':'post-form-description', 'rows':4, 'cols':35}),
            'live_link' : URLInput(attrs={'class':'post-form-link'}),
        }
