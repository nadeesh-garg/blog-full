from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
	user = UserSerializer(required = False)
	class Meta:
		model = Profile
		fields = ('url', 'user', 'pen_name', 'bio', 'birth_date', 'id', 'image')
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