from django.shortcuts import render
from .models import Blog
from userprofile.models import Profile
from user_responses.models import User_Responses
from blogseries.serializers import *
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from tagulous.models import SingleTagField, TagField
#API Endpoint for blog sets

class BlogViewSet(viewsets.ModelViewSet):
	#Returns All Publishable Blogs
	queryset = Blog.objects.filter(publishable=True).order_by('pub_date')
	permission_classes = [IsAuthenticatedOrReadOnly]
	#lookup_value_regex = '[0-9a-f]{32}'
	#lookup_value_regex = '[^/]+'
	lookup_field = 'slug'
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

class BlogListViewSet(viewsets.ModelViewSet):
	#TODO: Remove this queryset
	queryset = Blog.objects.filter(pk = 0).order_by('pub_date')
	permission_classes = [IsAuthenticatedOrReadOnly]
	serializer_class= BlogListSerializer
	#lookup_field = 'slug'
	def get_queryset(self):
		try:
			if(self.request.query_params['seriesslug'] != 'undefined' and self.request.query_params['userId'] == 'undefined'):
				seriesslug = self.request.query_params['seriesslug']
				ser = Series.objects.get(slug = seriesslug)
				return Blog.objects.filter(series = ser).filter(publishable = True).order_by('pub_date')
			elif(self.request.query_params['userId'] != 'undefined'):
				try:
					userId = int(self.request.query_params['userId'])
					userprof = Profile.objects.filter(pk = userId)
				except ValueError:
					user_slug=self.request.query_params['userId']
					userprof = Profile.objects.filter(slug = user_slug)
				return Blog.objects.filter(author = userprof).filter(publishable = True).order_by('pub_date')
			else:
				return Blog.objects.filter(publishable = True).order_by('pub_date')
		except KeyError:
			return Blog.objects.filter(publishable = True).order_by('pub_date')


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def blog_url_list(request, format=None):
	#A View that returns a list of urls of all blog/gallery objects to use random post
	blog_list = Blog.objects.filter(publishable=True).order_by('pub_date')
	arr_list = []
	for blog in blog_list:
		if(blog.series == None):
			serId = -1
			serSlug = ''
			serTitle = ''
		else:
			serId = blog.series.id
			serSlug = blog.series.slug
			serTitle = blog.series.title
		arr_list.append({'title':blog.title, 'slug':blog.slug, 'id':blog.id, 'series':{'id':serId, 'slug': serSlug, 'title': serTitle}})
	jsonresponse = arr_list
	return Response(jsonresponse)


class SeriesViewSet(viewsets.ModelViewSet):
	"""
    API endpoint that allows series to be viewed or edited.
    """
    #TODO: Filter to only series with more than one existing blog
	queryset = Series.objects.filter(pk=0).order_by('create_date')
	serializer_class = BlogSeriesSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]
	lookup_field = 'slug'
	def get_queryset(self):
		try:
			if(self.request.query_params['userId'] != 'undefined'):
				userId = int(self.request.query_params['userId'])
				userprof = Profile.objects.filter(slug = userId)
				return Series.objects.filter(creator = user).filter(publishable = True).order_by('pub_date')
			else:
				return Series.objects.all().order_by('create_date')
		except KeyError:
			return Series.objects.all().order_by('create_date')


	
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

@api_view(['POST'])
@permission_classes((AllowAny, ))
def UserResponseView(request):
	data = request.data
	try:
		if(request.data['response'] != '0'):
			blog = Blog.objects.get(slug = request.data['slug'])
			if(request.data['response'] > 0):
				blog.pos_responses += int(request.data['response'])
			else:
				blog.neg_responses -= int(request.data['response'])
			if(request.data['emailId'] != 'undefined' and request.data['emailId'] != None):
				user_response = User_Responses(userEmailId=request.data['emailId'], blog=blog)
				dupl_response = User_Responses.objects.filter(userEmailId=request.data['emailId'], blog=blog)
			elif(request.data['userFbId'] != 'undefined' and request.data['userFbId'] != None):
				user_response = User_Responses(userFbId=request.data['userFbId'], blog=blog, otherdata=request.data['otherdata'])
				dupl_response = User_Responses.objects.filter(userFbId=request.data['userFbId'], blog=blog)
			elif(request.data['userGoogleId'] != 'undefined' and request.data['userGoogleId'] != None):
				user_response = User_Responses(userGoogleId=request.data['userGoogleId'], blog=blog, otherdata=request.data['otherdata'])
				dupl_response = User_Responses.objects.filter(userGoogleId=request.data['userGoogleId'], blog=blog)
			else:
				return(Response({"Failed": "No User Detail"}, status=status.HTTP_400_BAD_REQUEST))
			if(len(dupl_response)>2):
				return(Response({"Failed": "Repeat Request from same ID"}, status=status.HTTP_409_CONFLICT))
			blog.save()
			user_response.response = int(request.data['response'])
			user_response.save()
			return(Response({"Success": "You are Studboy"}, status=status.HTTP_201_CREATED))
		else:
			return(Response({"Failed": "Response 0"}, status=status.HTTP_400_BAD_REQUEST))
	except KeyError:
		return(Response({"Failed": "Empty Body"}, status=status.HTTP_400_BAD_REQUEST))			
