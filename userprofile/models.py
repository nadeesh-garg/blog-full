from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete= models.CASCADE)
	pen_name = models.CharField(max_length=100, blank = True)
	bio = models.TextField(max_length=500, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	image = models.ImageField(upload_to="profile_images", blank=True)
	def __str__(self):
		return((self.user.first_name + " " + self.user.last_name + " | " + self.pen_name))
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