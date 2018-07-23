from django.contrib import admin
from .models import Profile
# Register your models here

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

class UserProfileInline(admin.StackedInline):
	model = Profile
	readonly_fields = ['slug']
	max_num = 1
	can_delete = False	

class UserAdmin(AuthUserAdmin):
	def add_view(self, *args, **kwargs):
		self.inlines = []
		return super(UserAdmin, self).add_view(*args, **kwargs)

	def change_view(self, *args, **kwargs):
		self.inlines = [UserProfileInline]
		return super(UserAdmin, self).change_view(*args, **kwargs)

# unregister old user admin
admin.site.unregister(User)
# register new user admin
admin.site.register(User, UserAdmin)
