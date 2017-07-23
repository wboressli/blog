from django.db import models

class Post(models.Model):
	title = models.CharField(max_length=50)
	content = models.TextField()
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.title

class Pizza(models.Model):
	editor_name = models.CharField(max_length=20)
	birth_date = models.DateField()

	def __str__(self):
		return self,editor_name