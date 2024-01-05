from rest_framework import serializers

from .models import Person, Color

from django.contrib.auth.models import User




class RegisterSerializer(serializers.Serializer):

	username = serializers.CharField()
	email = serializers.EmailField()
	password = serializers.CharField()

	def validate(self, data):

		# username = data.get('username', None)
		# email = data.get('email', None)

		if data['username']:
			if User.objects.filter(username=data['username']).exists():
				raise serializers.ValidationError('username is taken')

		if data['email']:
			if User.objects.filter(email=data['email']).exists():
				raise serializers.ValidationError('email is taken')

		return data


	def create(self, validated_data):

		user = User.objects.create(username = validated_data['username'], email = validated_data.get('email'))
		user.set_password(validated_data['password'])
		user.save()
		print(validated_data)
		return validated_data



class ColorSerializer(serializers.ModelSerializer):

	class Meta:
		model = Color
		fields = ['color_name']



class LoginSerializer(serializers.Serializer):

	username = serializers.CharField()
	password = serializers.CharField()



class PeopleSerializer(serializers.ModelSerializer):

	color = ColorSerializer()
	color_info = serializers.SerializerMethodField()

	class Meta:
		model = Person
		fields = '__all__'
		#depth = 1

	def get_color_info(self, obj):

		if obj.color:

			color_obj = Color.objects.get(id=obj.color.id)
			return {'color_name': color_obj.color_name, 'hex_code': '#000'}

		else:

			return {'color_name': 'No Color', 'hex_code': '#000'}


	def validate(self, data):

		special_characters = "!@#$%^&*()-+?_=,<>/"
		if any(c in special_characters for c in data['name']):
			raise serializers.ValidationError('name cannot contain special chars')

		if data.get('age') and data['age'] < 18:
			raise serializers.ValidationError('age should be greator than 18')

		return data