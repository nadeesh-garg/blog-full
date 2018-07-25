from django.contrib import admin
from .models import Profile
# Register your models here
#from django_summernote.admin import SummernoteModelAdmin
from django_summernote.widgets import SummernoteWidget
#from django.contrib.auth.models import User
#from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

class ProfileAdmin(admin.ModelAdmin):
	model = Profile
	readonly_fields = ['slug', 'user']
	max_num = 1
	can_delete = False
	list_display=["pen_name"]
	def user_link(self, obj):
		return '<a href="%s">%s</a>' % (
			urlresolvers.reverse('admin:userprofile_profile_change', args=(obj.user.id,)), obj.user)
	user_link.allow_tags = True
	user_link.short_description = 'User'

	def formfield_for_dbfield(self, db_field, **kwargs):
		if db_field.name == 'bio_full':
			kwargs['widget'] = SummernoteWidget()
		return super(ProfileAdmin,self).formfield_for_dbfield(db_field,**kwargs)
	def get_queryset(self, request):
		qs = super(ProfileAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(id=request.user.profile.id)
	def has_change_permission(self, request, obj=None):
		if obj is not None and obj.user != request.user and not request.user.is_superuser:
			return False
		return True
	def has_delete_permission(self, request, obj=None):
		if obj is not None and obj.user != request.user and not request.user.is_superuser:
			return False
		return True
		

admin.site.register(Profile, ProfileAdmin)

'''
class UserAdmin(AuthUserAdmin):
	def add_view(self, *args, **kwargs):
		self.inlines = []
		return super(UserAdmin, self).add_view(*args, **kwargs)

	def change_view(self, *args, **kwargs):
		self.inlines = [UserProfileInline]
		return super(UserAdmin, self).change_view(*args, **kwargs)
	def get_queryset(self, request):
		qs = super(UserAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(id=request.user.id)
# unregister old user admin
#admin.site.unregister(User)
# register new user admin
#admin.site.register(User, UserAdmin)
'''
