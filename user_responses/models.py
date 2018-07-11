from django.db import models
from blogseries.models import Blog, Series

# Create your models here.

class User_Responses(models.Model):
	blog = models.ForeignKey(Blog)
	#user = models.ForeignKey(User)
	userFbId = models.TextField(default = '')
	userGoogleId = models.TextField(default = '')
	userEmailId = models.TextField(default = '')
	response = models.IntegerField(default = 0)
	otherdata = models.TextField(blank=True)