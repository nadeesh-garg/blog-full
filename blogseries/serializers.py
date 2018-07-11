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
	#blog_set = serializers.HyperlinkedIdentityField(view_name="blog-detail", lookup_field='slug')
	class Meta:
		model = Series
		fields = ('url', 'title', 'genre', 'creator', 'create_date', 'slug', 'image', 'blog_set')
		lookup_field = 'slug'
		extra_kwargs = {'url': {'lookup_field': 'slug'}}
		

class BlogSerializer(serializers.HyperlinkedModelSerializer):

	series = BlogSeriesSerializer(required = False)
	author = UserProfileSerializer()
	tags = TagFieldSerializer(many =True)
	class Meta:
		model = Blog
		fields = ('url', 'folder', 'slug', 'series', 'author', 'title', 'pub_date', 'tags', 'description', 'content', 'hidden_message', 'welcome_image', 'publishable', 'pos_responses', 'neg_responses')
		lookup_field = 'slug'
		extra_kwargs = {'url': {'lookup_field': 'slug'}}
		

class BlogListSerializer(serializers.HyperlinkedModelSerializer):
	#url = serializers.HyperlinkedIdentityField(view_name="blog-list",
	#											lookup_field = "slug")
	series = BlogSeriesSerializer(required=False)
	author = UserProfileSerializer()
	tags = TagFieldSerializer(many =True)

	class Meta:
		model = Blog
		fields = ('folder', 'slug', 'series', 'author', 'title', 'pub_date', 'tags', 'description', 'welcome_image', 'publishable', 'pos_responses', 'neg_responses')
		#lookup_field = 'slug'
		#extra_kwargs = {'url': {'lookup_field': 'slug', 'view_name': 'blog-list' }}
		
class SeriesSerializer(serializers.HyperlinkedModelSerializer):
	creator = UserProfileSerializer()
	#tags = TagFieldSerializer()
	genre = SingleTagFieldSerializer()
	blog_set = BlogListSerializer()
	class Meta:
		model = Series
		fields = ('url', 'title', 'genre', 'creator', 'create_date', 'slug', 'image', 'blog_set')
		lookup_field = 'slug'
		extra_kwargs = {'url': {'lookup_field': 'slug'}}
		
