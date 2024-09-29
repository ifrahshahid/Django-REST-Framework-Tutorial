# views.py

# -------------------Using dataclasses.py----------------------

from snippets.models import Snippet
from snippets.dataclasses import SnippetData, UserData, serialize_snippet, serialize_user
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework import renderers

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        users = self.queryset
        user_data = [UserData.from_model(user, request) for user in users]
        return Response([serialize_user(user) for user in user_data]) 

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def list(self, request, *args, **kwargs):
        snippets = self.queryset
        snippet_data = [SnippetData.from_model(snippet, request) for snippet in snippets]
        return Response([serialize_snippet(snippet) for snippet in snippet_data])  

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# -------------------Using serializers.py-------------------------------


# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer, UserSerializer
# from rest_framework import generics
# from django.contrib.auth.models import User
# from rest_framework import permissions
# from snippets.permissions import IsOwnerOrReadOnly
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.reverse import reverse
# from rest_framework import renderers
# from rest_framework import permissions
# from rest_framework import renderers
# from rest_framework.decorators import action
# from rest_framework.response import Response


# from rest_framework import viewsets


# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     This viewset automatically provides `list` and `retrieve` actions.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class SnippetViewSet(viewsets.ModelViewSet):
#     """
#     This ViewSet automatically provides `list`, `create`, `retrieve`,
#     `update` and `destroy` actions.

#     Additionally we also provide an extra `highlight` action.
#     """
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly]

#     @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
#     def highlight(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)