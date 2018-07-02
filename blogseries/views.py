from django.shortcuts import render
from .models import Blog
from blogseries.serializers import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from tagulous.models import SingleTagField, TagField
#API Endpoint for blog sets

class BlogViewSet(viewsets.ModelViewSet):
	#Returns All Publishable Blogs
	queryset = Blog.objects.filter(publishable=True).order_by('pub_date')
	permission_classes = [IsAuthenticatedOrReadOnly]
	serializer_class = BlogSerializer
	action_serializers = {
        'retrieve': BlogSerializer,
        'list': BlogListSerializer,
        'create': BlogSerializer
    }
	def get_serializer_class(self):
		if hasattr(self, 'action_serializers'):
			if self.action in self.action_serializers:
				return self.action_serializers[self.action]
		return super(BlogViewSet, self).get_serializer_class()
'''
class BlogViewSet(viewsets.ModelViewSet):
	queryset = Blog.objects.all().order_by('pub_date')
	permission_classes = [IsAuthenticatedOrReadOnly]
	serializer_class = BlogSerializer
'''
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def blog_url_list(request, format=None):
	#A View that returns a list of urls of all blog/gallery objects to use random post
	blog_list = Blog.objects.filter(publishable=True).order_by('pub_date')
	arr_list = []
	for blog in blog_list:
		arr_list.append({'name':blog.title, 'link':blog.slug, 'id':blog.id})
	jsonresponse = {'data':arr_list}
	return Response(jsonresponse)


class SeriesViewSet(viewsets.ModelViewSet):
	"""
    API endpoint that allows series to be viewed or edited.
    """
	queryset = Series.objects.all().order_by('create_date')
	serializer_class = BlogSeriesSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]
	
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def AllTagsView(request, format=None):
	"""
    API endpoint that allows tags to be viewed or edited.
    """
	tags_list = Blog.tags.tag_model.objects.all().order_by('-count')
	arr_list=[]
	for tag in tags_list:
		arr_list.append({'name':tag.name, 'count':tag.count})
	jsonresponse = {'data':arr_list}
	return Response(jsonresponse)
	#permission_classes = [IsAuthenticatedOrReadOnly]

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def AllGenresView(request, format=None):
	"""
    API endpoint that allows tags to be viewed or edited.
    """
	tags_list = Series.genre.tag_model.objects.all().order_by('-count')
	arr_list=[]
	for tag in tags_list:
		arr_list.append({'name':tag.name, 'count':tag.count})
	jsonresponse = {'data':arr_list}
	return Response(jsonresponse)
	#permission_classes = [IsAuthenticatedOrReadOnly]
