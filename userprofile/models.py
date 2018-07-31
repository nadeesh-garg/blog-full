from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from utilities import unique_slug_generator
from tagulous.models import SingleTagField, TagField


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete= models.CASCADE)
	pen_name = models.CharField(max_length=100, unique=True)
	bio_summary = models.TextField(max_length=1000, blank=True)
	bio_full = models.TextField(blank=True)
	designation = models.CharField(max_length=100, blank=True, null=True)
	interests = TagField(force_lowercase = True, max_count = 10)
	birth_date = models.DateField(null=True, blank=True)
	image = models.ImageField(upload_to="profile_images", blank=True)
	slug = models.SlugField(max_length=100, unique=True)
	def __str__(self):
		return((self.user.first_name + " " + self.user.last_name + " | " + self.pen_name))
	def save(self, *args, **kwargs):
		if(not self.slug):
			self.slug = unique_slug_generator(self, 'user.username')
		super(Profile, self).save(*args, **kwargs)  # Call the "real" save() method.
			
	class Meta:
		permissions = (
			("is_moderator", "Can Moderate Others"),
			)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()