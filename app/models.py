from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # ForeignKey is used to coincide Event with User class 
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # Used to create a hyperlink on calendar to view event detail
    def get_html_url(self):
        url = reverse('app:event_detail', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
