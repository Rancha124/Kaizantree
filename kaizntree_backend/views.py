from django.contrib.auth.models import User
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from .models import Item, Category, Tag
from .serializers import ItemSerializer, CategorySerializer, TagSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Category
from django.utils.dateparse import parse_date
from datetime import datetime

# Existing viewsets for Item, Category, and Tag
# class ItemViewSet(ModelViewSet):
#     serializer_class = ItemSerializer

#     def get_queryset(self):
#         """
#         Optionally restricts the returned items to a given user,
#         by filtering against a `username` query parameter in the URL.
#         """
#         queryset = Item.objects.all()
#         search_query = self.request.query_params.get('search', None)

#         if search_query is not None:
#             queryset = queryset.filter(
#                 Q(name__icontains=search_query) |
#                 Q(sku__icontains=search_query) |
#                 Q(category__name__icontains=search_query) |  # Searches in category name
#                 Q(tags__name__icontains=search_query)  # Searches in tag names
#             ).distinct()  # Use distinct() to avoid duplicates when joining

#         # Handle ordering if needed
#         ordering = self.request.query_params.get('ordering', None)
#         if ordering:
#             queryset = queryset.order_by(ordering)

#         return queryset



class ItemViewSet(ModelViewSet):
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = Item.objects.all()
        search_query = self.request.query_params.get('search', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(sku__icontains=search_query) |
                Q(category__name__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()

        if start_date:
            start_date_parsed = parse_date(start_date)
            queryset = queryset.filter(created_at__date__gte=start_date_parsed)

        if end_date:
            end_date_parsed = parse_date(end_date)
            queryset = queryset.filter(created_at__date__lte=end_date_parsed)

        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer



@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'Login successful',
            'token': token.key
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'error': 'Invalid Credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    # Check if the username or email is already taken
    if User.objects.filter(username=username).exists():
        return Response({'message': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists():
        return Response({'message': 'Email is already in use.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create the user with the provided username, email, and password
    user = User.objects.create_user(username=username, email=email, password=password)
    
    # Optionally, create and return a token for the newly registered user
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'message': 'User created successfully',
        'token': token.key  # Optionally return the token as part of the registration response
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def list_items(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


