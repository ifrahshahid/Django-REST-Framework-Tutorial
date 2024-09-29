from django.urls import path, include
from rest_framework.routers import DefaultRouter

from snippets import views

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet, basename='snippet')
router.register(r'users', views.UserViewSet, basename='user')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]







# from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns
# from rest_framework import renderers

# from snippets.views import api_root, SnippetViewSet, UserViewSet

# # Map HTTP methods to actions for SnippetViewSet
# snippet_list = SnippetViewSet.as_view({
#     'get': 'list',         # HTTP GET -> list action
#     'post': 'create'       # HTTP POST -> create action
# })

# snippet_detail = SnippetViewSet.as_view({
#     'get': 'retrieve',      # HTTP GET -> retrieve a single snippet
#     'put': 'update',        # HTTP PUT -> update a snippet
#     'patch': 'partial_update', # HTTP PATCH -> partially update a snippet
#     'delete': 'destroy'     # HTTP DELETE -> delete a snippet
# })

# snippet_highlight = SnippetViewSet.as_view({
#     'get': 'highlight'      # HTTP GET -> custom highlight action
# }, renderer_classes=[renderers.StaticHTMLRenderer]) # Use StaticHTMLRenderer for this view

# # Map HTTP methods to actions for UserViewSet
# user_list = UserViewSet.as_view({
#     'get': 'list'           # HTTP GET -> list users
# })

# user_detail = UserViewSet.as_view({
#     'get': 'retrieve'       # HTTP GET -> retrieve user details
# })

# # Define the URL patterns and include the api_root as the base
# urlpatterns = format_suffix_patterns([
#     path('', api_root, name='api-root'),                       # Root of the API
#     path('snippets/', snippet_list, name='snippet-list'),      # List and create snippets
#     path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),  # Snippet details, update, delete
#     path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'), # Highlight action
#     path('users/', user_list, name='user-list'),               # List users
#     path('users/<int:pk>/', user_detail, name='user-detail')   # User details
# ])
