from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated

from moviesapp.serializers import UserSerializer, PagedMoviesSerializer
from moviesapp.utils import fetch_with_retries
from .models import Movie, Collection
from .serializers import CollectionSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({'access_token': access_token}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_list(request):
    try:
        data = fetch_with_retries('https://demo.credy.in/api/v1/maya/movies/')
    except Exception as e:
        return Response({'detail': 'Failed to fetch movies.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    serializer = PagedMoviesSerializer(data=data)
    if serializer.is_valid():
        return Response(serializer.data)
    else:
        return Response({'detail': 'Failed to serialize movies.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def collection_list(request):
    if request.method == 'GET':
        collections = Collection.objects.filter(user=request.user)
        serializer = CollectionSerializer(collections, many=True)

        movies = Movie.objects.filter(collection__in=collections)

        if movies:
            genres_dict = {}
            for movie in movies:
                for genre in movie.genres.split(','):
                    genre = genre.strip()
                    if genre in genres_dict:
                        genres_dict[genre] += 1
                    else:
                        genres_dict[genre] = 1
            top_genres = dict(sorted(genres_dict.items(), key=lambda item: item[1], reverse=True))
            top_3_genres = [genre for genre, count in sorted(genres_dict.items(), key=lambda item: item[1], reverse=True)[:3]]
        else:
            top_3_genres = []

        response_data = {
            'is_success': True,
            'data': {
                'collections': serializer.data,
                'favourite_genres': top_3_genres
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            collection = serializer.save(user=request.user)
            response_data = {
                'collection_uuid': collection.uuid
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def edit_collection(request, collection_uuid):
    if request.method == 'GET':
        try:
            collection = Collection.objects.get(uuid=collection_uuid, user=request.user)
        except Collection.DoesNotExist:
            return Response({'detail': 'Collection not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CollectionSerializer(collection)
        
        return Response({
            'title': serializer.data['title'],
            'description': serializer.data['description'],
            'movies': serializer.data['movies']
        }, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        collection = get_object_or_404(Collection, uuid=collection_uuid, user=request.user)

        serializer = CollectionSerializer(collection, data=request.data, partial=True)
        if serializer.is_valid():
            updated_collection = serializer.save()
            response_data = {
                'collection_uuid': updated_collection.uuid
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        collection = get_object_or_404(Collection, uuid=collection_uuid, user=request.user)
        collection.delete()
        return Response({'message': 'Collection deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_request_count(request):
    count = cache.get('request_count', 0)
    return JsonResponse({'requests': count})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_request_count(request):
    # Reset the request count in Redis
    cache.set('request_count', 0)
    return JsonResponse({'message': 'request count reset successfully'})