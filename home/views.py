from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Person
from .serializers import PeopleSerializer, LoginSerializer, RegisterSerializer

from rest_framework.views import APIView

from rest_framework import viewsets

from rest_framework import status

from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token

from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import TokenAuthentication

from django.core.paginator import Paginator

from rest_framework.decorators import action



class LoginAPI(APIView):

	def post(self, request):

		data = request.data

		serializer = LoginSerializer(data=data)
		print(serializer)

		if not serializer.is_valid():
			return Response({
				'status': 'False',
				'message': serializer.errors
				}, status.HTTP_400_BAD_REQUEST)

		user = authenticate(username = serializer.data['username'], password = serializer.data['password'])

		if not user:
			return Response({
				'status': 'False',
				'message': "Invalid Credential"
				}, status.HTTP_400_BAD_REQUEST)

		token, _ = Token.objects.get_or_create(user=user)

		return Response({
			'status': 'True',
			'message': 'user login',
			'token': str(token)
			}, status.HTTP_201_CREATED)


class registerAPI(APIView):

	def post(self, request):

		data = request.data
		serializer = RegisterSerializer(data=data)

		if not serializer.is_valid():
			return Response({
				'status': 'False',
				'message': serializer.errors
				}, status.HTTP_400_BAD_REQUEST)

		serializer.save()
		return Response({
			'status': 'True',
			'message': 'user created'
			}, status.HTTP_201_CREATED)

# {"username": "Chetan", "email": "chetan@gmail.com", "password": 1234}


@api_view(['GET', 'POST'])
def index(request):

	if request.method == 'GET':
		print(request.GET.get('format'))
		json_response = {
			'name' : 'Scaler',
			'courses' : ['C++', 'Python'],
			'method' : 'GET'
			}
		print(request.GET.get('search'))

	else:
		data = request.data
		print("okk",data["name"])
		json_response = {
			'name' : 'Scaler',
			'courses' : ['C++', 'Python'],
			'method' : 'POST'
			}


	return Response(json_response)


@api_view(['POST'])
def login(request):

	data = request.data
	serializer = LoginSerializer(data=data)

	if serializer.is_valid():

		data = serializer.data
		print(data)
		return Response({'message': 'success'})

	return Response(serializer.errors)


class PersonAPI(APIView):

	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]

	def get(self, request):

		obj = Person.objects.filter(color__isnull = False)

		page = request.GET.get('page', 1)
		page_size = 3
		paginator = Paginator(obj, page_size)

		serializer = PeopleSerializer(paginator.page(page), many=True)

		return Response(serializer.data)

		# return Response({"message": "This is a get request"})

	def post(self, request):

		data = request.data
		serializer = PeopleSerializer(data=data)

		if serializer.is_valid():

			serializer.save()

			return Response(serializer.data)

		return Response(serializer.errors)

	def put(self, request):

		data = request.data

		obj = Person.objects.get(id = data['id'])

		serializer = PeopleSerializer(obj, data=data)

		if serializer.is_valid():

			serializer.save()

			return Response(serializer.data)

		return Response(serializer.errors)

	def patch(self, request):

		data = request.data
		obj = Person.objects.get(id=data['id'])

		serializer = PeopleSerializer(obj, data=data, partial=True)
		if serializer.is_valid():

			serializer.save()

			return Response(serializer.data)

		return Response(serializer.errors)

	def delete(self, request):

		data = request.data

		try:
		    id_value = data['id']
		    obj = Person.objects.get(id=id_value)
		    obj.delete()
		    return Response({'message': 'Person Deleted'})
		except (KeyError, Person.DoesNotExist):
		    return Response({'message': 'Missing or invalid id'})



@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def person(request):

	if request.method == 'GET':

		try:

			obj = Person.objects.all()

			page = request.GET.get('page', 1)
			page_size = 3
			

			paginator = Paginator(obj, page_size)
			serializer = PeopleSerializer(paginator.page(page), many=True)

			return Response(serializer.data)
			
		except Exception as e:
			return Response({
				"status": False,
				"message": "Invaid page"
				})

	elif request.method == 'POST':

		data = request.data
		serializer = PeopleSerializer(data=data)
		if serializer.is_valid():

			serializer.save()

			return Response(serializer.data)

		return Response(serializer.errors)

	elif request.method == 'PUT':

		data = request.data
		obj = Person.objects.get(id = data['id'])
		serializer = PeopleSerializer(obj, data=data)
		if serializer.is_valid():

			serializer.save()

			return Response(serializer.data)

		return Response(serializer.errors)

	elif request.method == 'PATCH':

		data = request.data
		obj = Person.objects.get(id = data['id'])
		serializer = PeopleSerializer(obj, data=data, partial=True)
		if serializer.is_valid():

			serializer.save()

			return Response(serializer.data)

		return Response(serializer.errors)

	else:
		
		try:
		    id = request.GET.get('id')
		    obj = Person.objects.get(id=id_value)
		    obj.delete()
		    return Response({'message': 'Person Deleted'})
		except (KeyError, Person.DoesNotExist):
		    return Response({'message': 'Missing or invalid id'})






class PeopleViewSet(viewsets.ModelViewSet):

	serializer_class = PeopleSerializer

	queryset = Person.objects.all()

	http_method_names = ['get', 'post']

	def list(self, request):

		search = request.GET.get('search')
		queryset = self.queryset

		if search:

			queryset = queryset.filter(name__startswith = search)

		serializer = PeopleSerializer(queryset, many=True)
		return Response({'status': 200, 'data': serializer.data}, status=status.HTTP_200_OK)

	@action(detail=True, methods=['get'])
	def send_mail_to_person(self, request, pk):

		obj = Person.objects.get(pk=pk)
		serializer = PeopleSerializer(obj)

		return Response({
	 		"status": True,
	 		"message": "email send Successfully",
	 		"data": serializer.data
	 		})
