from django.contrib import admin
from django_summernote.widgets import SummernoteWidget
from .models import Series, Blog
# Register your models here.

# Apply summernote to all TextField in model.
class SomeModelAdmin(admin.ModelAdmin):  # instead of ModelAdmin
	exclude = ["slug"]
	readonly_fields = ('creator', "create_date")
	def get_queryset(self, request):
		qs = super(SomeModelAdmin, self).get_queryset(request)
		if request.user.is_superuser or request.user.has_perm("userprofile.is_moderator"):
			return qs
		return qs.filter(creator=request.user.profile)
	def save_model(self, request, obj, form, change):
		if obj is not None and not request.user.is_superuser and not request.user.has_perm("userprofile.is_moderator"):
			obj.creator = request.user.profile
		elif obj.creator_id == None:
			obj.creator = request.user.profile
		super(SomeModelAdmin, self).save_model(request, obj, form, change)
	def has_change_permission(self, request, obj=None):
		if obj is not None and obj.creator.user != request.user and not request.user.is_superuser and not request.user.has_perm("userprofile.is_moderator"):
			return False
		return True
	def has_delete_permission(self, request, obj=None):
		if obj is not None and obj.creator.user != request.user and not request.user.is_superuser and not request.user.has_perm("userprofile.is_moderator"):
			return False
		return True
	
	

class BlogModelAdmin(admin.ModelAdmin):
	exclude = ["slug", "create_date"]
	readonly_fields = ["author", "pub_date", "pos_responses", "neg_responses"]
	actions = ["mark_publishable"]
	list_per_page = 25
	list_display=('title', 'publishable', 'pos_responses', 'neg_responses')
	def formfield_for_dbfield(self, db_field, **kwargs):
		if db_field.name == 'content':
			kwargs['widget'] = SummernoteWidget()
		return super(BlogModelAdmin,self).formfield_for_dbfield(db_field,**kwargs)
	def mark_publishable(self, request, queryset):
		queryset.update(publishable=True)
	def get_queryset(self, request):
		qs = super(BlogModelAdmin, self).get_queryset(request)
		if request.user.is_superuser or request.user.has_perm("userprofile.is_moderator"):
			return qs
		return qs.filter(author=request.user.profile)
	def save_model(self, request, obj, form, change):
		#import pdb; pdb.set_trace()
		if obj is not None and not request.user.is_superuser and not request.user.has_perm("userprofile.is_moderator"):
			obj.author = request.user.profile
		elif obj.author_id == None:
			obj.author = request.user.profile
		super(BlogModelAdmin, self).save_model(request, obj, form, change)
	def has_change_permission(self, request, obj=None):
		if obj is not None and obj.author.user != request.user and not request.user.is_superuser and not request.user.has_perm("userprofile.is_moderator"):
			return False
		return True
	def has_delete_permission(self, request, obj=None):
		if obj is not None and obj.author.user != request.user and not request.user.is_superuser and not request.user.has_perm("userprofile.is_moderator"):
			return False
		return True
	

admin.site.register(Series, SomeModelAdmin)
admin.site.register(Blog, BlogModelAdmin)
