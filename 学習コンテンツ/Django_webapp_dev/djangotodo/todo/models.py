from django.db import models

# Create your models here.

class TodoModel(models.Model):
	title = models.CharFIeld(max_length=100)
	memo = models.TextField()
