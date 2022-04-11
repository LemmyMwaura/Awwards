from django.forms import ClearableFileInput, EmailField, EmailInput, ModelForm, NumberInput, TextInput, Textarea,URLInput, CharField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Project, Rating
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

class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = '__all__'
        exclude = ['updated','created','project','rated_by']
        widgets = {
            'creativity':NumberInput(attrs={'class':'rating-creativity'}),
            'design':NumberInput(attrs={'class':'rating-design'}),
            'usability':NumberInput(attrs={'class':'rating-usability'}),
            'content':NumberInput(attrs={'class':'rating-content'}),
        }

class UserRegistrationForm(UserCreationForm):
    first_name = CharField(max_length=50, widget=TextInput(attrs={'class':'new-user-firstname'}))
    last_name = CharField(max_length=50, widget=TextInput(attrs={'class':'new-user-lastname'}))
    email = EmailField(widget=EmailInput(attrs={'class':'new-user-email'}))
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs={'class' : 'new-user-username'}
        self.fields['password1'].widget.attrs={'class' : 'new-user-password'}
        self.fields['password2'].widget.attrs={'class': 'new-user-confirm-password'}