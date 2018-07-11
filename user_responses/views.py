from django.shortcuts import render

# Create your views here.

'''The Following Views will be created here:
1) Receives a request given bound object and returns rating etc. data
2) Receives UserProfile data and returns Object, rating etc. data 
'''
@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def rating_view(request, format=None):
	#A View used to rate a post/object: Get what something is in request.
	
	return Response()
