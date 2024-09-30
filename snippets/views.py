# views.py

# -------------------Using dataclasses.py----------------------

from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from snippets.models import Snippet
from django.contrib.auth.models import User
from snippets.dataclasses import SnippetData, UserData
from snippets.permissions import IsOwnerOrReadOnly
from django.urls import reverse

def build_snippet_response(request, snippet):
    """Helper function to build snippet response data with absolute URLs."""
    return SnippetData(
        url=request.build_absolute_uri(reverse('snippet-detail', args=[snippet.id])),
        id=snippet.id,
        highlight=request.build_absolute_uri(reverse('snippet-highlight', args=[snippet.id])),
        owner=snippet.owner.username,
        title=snippet.title,
        code=snippet.code,
        linenos=snippet.linenos,
        language=snippet.language,
        style=snippet.style
    ).to_dict()

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def snippet_list(request):
    """
    List all snippets or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        data = [build_snippet_response(request, snippet) for snippet in snippets]
        return Response(data)

    elif request.method == 'POST':
        snippet = Snippet.objects.create(
            owner=request.user,
            title=request.data.get('title'),
            code=request.data.get('code'),
            linenos=request.data.get('linenos', False),
            language=request.data.get('language'),
            style=request.data.get('style'),
        )
        return Response(build_snippet_response(request, snippet), status=201)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly])
def snippet_detail(request, pk):
    """
    Retrieve, update, or delete a snippet.
    """
    snippet = get_object_or_404(Snippet, pk=pk)

    if request.method == 'GET':
        return Response(build_snippet_response(request, snippet))

    elif request.method in ['PUT', 'PATCH']:
        for attr in ['title', 'code', 'linenos', 'language', 'style']:
            if attr in request.data:
                setattr(snippet, attr, request.data[attr])
        snippet.save()
        return Response(build_snippet_response(request, snippet))

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=204)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def snippet_highlight(request, pk):
    """
    Highlight a snippet.
    """
    snippet = get_object_or_404(Snippet, pk=pk)
    highlighted_code = snippet.highlighted  
    return Response(highlighted_code, content_type='text/html')

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def user_list(request):
    """
    List all users.
    """
    users = User.objects.all()
    data = [
        UserData(
            url=request.build_absolute_uri(reverse('user-detail', args=[user.id])),
            id=user.id,
            username=user.username,
            snippets=[
                request.build_absolute_uri(reverse('snippet-detail', args=[snippet.id])) 
                for snippet in user.snippet_set.all()
            ]
        ).to_dict()
        for user in users
    ]
    return Response(data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def user_detail(request, pk):
    """
    Retrieve a user by ID.
    """
    user = get_object_or_404(User, pk=pk)
    data = UserData(
        url=request.build_absolute_uri(reverse('user-detail', args=[user.id])),
        id=user.id,
        username=user.username,
        snippets=[
            request.build_absolute_uri(reverse('snippet-detail', args=[snippet.id])) 
            for snippet in user.snippet_set.all()
        ]
    ).to_dict()
    return Response(data)


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


