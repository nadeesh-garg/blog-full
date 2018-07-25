from .models import Blog, Series
from rest_framework import serializers
from userprofile.serializers import UserProfileSerializer
from tagulous.models import SingleTagField as SingleTagModel
#from tagulous.models import TagField as TagModel
#from tagulous.forms import SingleTagField, TagField

class BlogTagFieldSerializer(serializers.ModelSerializer):
	#tags = serializers.SerializerMethodField()
	class Meta:
		model = Blog.tags.tag_model
		fields = ('name', 'count')
		depth = 1
	#fields = ('name', 'count')
class SeriesTagFieldSerializer(serializers.ModelSerializer):
	class Meta:
		model = Series.genre.tag_model
		fields = ('name', 'count')
		depth = 1


class BlogSeriesSerializer(serializers.HyperlinkedModelSerializer):
	creator = UserProfileSerializer()
	#tags = TagFieldSerializer()
	genre = SeriesTagFieldSerializer(many=True)
	#blog_set = serializers.HyperlinkedIdentityField(view_name="blog-detail", lookup_field='slug')
	class Meta:
		model = Series
		fields = ('url', 'title', 'genre', 'creator', 'create_date', 'slug', 'image', 'blog_set', 'description')
		lookup_field = 'slug'
		extra_kwargs = {'url': {'lookup_field': 'slug'}}
		

class BlogSerializer(serializers.HyperlinkedModelSerializer):

	series = BlogSeriesSerializer(required = False)
	author = UserProfileSerializer()
	tags = BlogTagFieldSerializer(many =True)
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
	tags = BlogTagFieldSerializer(many =True)

	class Meta:
		model = Blog
		fields = ('folder', 'slug', 'series', 'author', 'title', 'pub_date', 'tags', 'description', 'welcome_image', 'publishable', 'pos_responses', 'neg_responses')
		#lookup_field = 'slug'
		#extra_kwargs = {'url': {'lookup_field': 'slug', 'view_name': 'blog-list' }}
		

		
