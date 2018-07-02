from django.db import models
from mywebsite.blogseries.models import Blog, Series

# Create your models here.

class User_Responses(models.Model):
	#binding_to = models.ForeignKey(Blog)
	#user = models.ForeignKey(User)
	content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    binding_to = GenericForeignKey('content_type', 'object_id')
    claps = models.PositiveIntegerField(default = 0)
    originality = models.FloatField(default = 0.0)
    skill = models.FloatField(default = 0.0)