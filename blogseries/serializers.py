from .models import Blog, Series
from rest_framework import serializers
from userprofile.serializers import UserProfileSerializer
from tagulous.models import SingleTagField as SingleTagModel
#from tagulous.models import TagField as TagModel
#from tagulous.forms import SingleTagField, TagField

class TagFieldSerializer(serializers.ModelSerializer):
	#tags = serializers.SerializerMethodField()
	class Meta:
		model = Blog.tags.tag_model
		fields = ('name', 'count')
		depth = 1
	#fields = ('name', 'count')
class SingleTagFieldSerializer(serializers.Serializer):
	class Meta:
		model = Series.genre.tag_model
		fields = ('name', 'count')


class BlogSeriesSerializer(serializers.HyperlinkedModelSerializer):
	creator = UserProfileSerializer()
	#tags = TagFieldSerializer()
	genre = SingleTagFieldSerializer()
	class Meta:
		model = Series
		fields = ('url', 'title', 'genre', 'creator', 'create_date', 'slug', 'image')

class BlogSerializer(serializers.HyperlinkedModelSerializer):
	series = BlogSeriesSerializer(required = False)
	author = UserProfileSerializer()
	tags = TagFieldSerializer(many =True)
	class Meta:
		model = Blog
		fields = ('url', 'folder', 'slug', 'series', 'author', 'title', 'pub_date', 'tags', 'description', 'content', 'hidden_message', 'welcome_image')

class BlogListSerializer(serializers.HyperlinkedModelSerializer):
	series = BlogSeriesSerializer(required=False)
	author = UserProfileSerializer()
	tags = TagFieldSerializer(many =True)
	class Meta:
		#extra_kwargs = {'url': {'view_name': 'blog-list'}}
		model = Blog
		fields = ('url', 'folder', 'slug', 'series', 'author', 'title', 'pub_date', 'tags', 'description', 'welcome_image')


