from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Profile

class UserTagFieldSerializer(serializers.ModelSerializer):
	#tags = serializers.SerializerMethodField()
	class Meta:
		model = Profile.interests.tag_model
		fields = ('name', 'count')
		depth = 1

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
	user = UserSerializer(required = False)
	interests= UserTagFieldSerializer(required = False, many=True)
	class Meta:
		model = Profile
		fields = ('url', 'pen_name', 'bio_summary', 'bio_full', 'designation', 'birth_date', 'slug', 'image', 'interests')
		lookup_field = 'slug'
		extra_kwargs = {'url': {'lookup_field': 'slug'}}
	def create(self, validated_data):
		user_data = validated_data.pop('user')
		profile = Profile.objects.create(**validated_data)
		User.objects.create(profile = profile, **user_data)
		profile.save()
		return profile

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')