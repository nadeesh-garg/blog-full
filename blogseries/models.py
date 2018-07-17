from django.db import models
from tagulous.models import SingleTagField, TagField
from userprofile.models import Profile
from datetime import datetime
from utilities import unique_slug_generator
# Create your models here.

class Series(models.Model):
	title = models.CharField(max_length=150)
	genre = SingleTagField(force_lowercase = True)
	description = models.CharField(max_length=255, blank = True, null=True)
	creator = models.ForeignKey(Profile, blank=True, null=True)
	#tags = TagField(force_lowercase = True, max_count = 10)
	create_date = models.DateTimeField(default=datetime.now, blank=True)
	slug = models.SlugField(unique=True, max_length=100, blank = True)
	image = models.ImageField(upload_to='series_images', blank = True, null=True)
	def __str__(self):
		return self.title
	def save(self, *args, **kwargs):
		if(not self.slug):
			self.slug = unique_slug_generator(self)
		super().save(*args, **kwargs)  # Call the "real" save() method.
			


class Blog(models.Model):
	BLOG = 'BL'
	GALLERY = 'GL'
	FOLDER_CHOICES = ((BLOG, 'Blog'), (GALLERY, 'Gallery'))
	welcome_image = models.ImageField(upload_to='blog_welcome', blank = True)
	author = models.ForeignKey(Profile)
	folder = models.CharField(max_length=2, choices = FOLDER_CHOICES, default = BLOG, blank = False)
	series = models.ForeignKey(Series, blank = True, null=True)
	title = models.CharField(max_length=150)
	description = models.CharField(max_length=255)
	tags = TagField(force_lowercase = True, max_count = 5)
	content = models.TextField(blank = True)
	hidden_message = models.CharField(max_length = 100, blank=True, null=True)
	publishable = models.BooleanField(default=False)
	slug = models.SlugField(unique=True, max_length=255, blank = True)
	create_date = models.DateTimeField(default=datetime.now, blank=True)
	pub_date = models.DateTimeField(blank=True, null=True)
	pos_responses = models.PositiveIntegerField(default = 0)
	neg_responses = models.PositiveIntegerField(default = 0)
	def __str__(self):
		return self.title
	def save(self, *args, **kwargs):
		if(not self.slug):
			self.slug = unique_slug_generator(self)
		if(self.publishable):
			self.pub_date = datetime.now()
		super().save(*args, **kwargs)  # Call the "real" save() method.
		#do_something_else()

	
	#additional_image = models.ImageField(upload_to='media', blank =True)

#class ContentImages(models.Model):
#	image = models.ImageField(upload_to='media', blank = True)

'''TODO for image and other content addition:
1) 	Create Image, caption, image_positioning_tag as singular object.
2) 	As soon as image is added (on same admin page as Blog), image_positioning tag should be added to cursor position in Blog.content
3) 	When Frontend recieves it, content is read uptil every occurance of image_tags, then image is animated/placed. Next, repeated. 
	Any stray images, without a tag will be placed at the end. 

Check Out following stackoverflow answer:
https://stackoverflow.com/questions/28326456/django-using-media-url-in-template-with-httpresponse
'''
