from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Series, Blog
# Register your models here.

# Apply summernote to all TextField in model.
class SomeModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    ...


admin.site.register(Series, SomeModelAdmin)
admin.site.register(Blog, SomeModelAdmin)
