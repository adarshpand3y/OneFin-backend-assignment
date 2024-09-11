from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view),
    path('movies/', views.movie_list),

    path('collection/', views.collection_list),
    path('collection/<uuid:collection_uuid>/', views.edit_collection),

    path('request-count/', views.get_request_count),
    path('request-count/reset/', views.reset_request_count),
]
