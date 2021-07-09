from django import forms
from .models import Event
from django.contrib.auth.models import User

# Model form of model 'User' inbuilt in Django
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(required=True, label='Email',
                    widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(max_length=20, label='Username',
                    widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    
    # Django Meta class used to transfer information about the model to the Django forms
    class Meta:
        model = User
        fields = ('username','email','password') # The generated Form class will have a form field for every model field specified, in the order specified in the fields attribute.

# Model form of model 'Event' in models.py
class EventForm(forms.ModelForm):
    # Django Meta class used to transfer information about the model to the Django forms
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    exclude = ['user'] # The exclude attribute tells Django what fields from the model not to include in the form.

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
