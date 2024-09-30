# from django.urls import path, include
# from rest_framework.routers import DefaultRouter

# from snippets import views

# # Create a router and register our ViewSets with it.
# router = DefaultRouter()
# router.register(r'snippets', views.SnippetViewSet, basename='snippet')
# router.register(r'users', views.UserViewSet, basename='user')

# # The API URLs are now determined automatically by the router.
# urlpatterns = [
#     path('', include(router.urls)),
# ]

from django.urls import path
from snippets import views

urlpatterns = [
    path('snippets/', views.snippet_list, name='snippet-list'),
    path('snippets/<int:pk>/', views.snippet_detail, name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', views.snippet_highlight, name='snippet-highlight'),
    path('users/', views.user_list, name='user-list'),
    path('users/<int:pk>/', views.user_detail, name='user-detail'),
]


