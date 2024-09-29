# views.py


# -------------------Using serializers.py-------------------------------


from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response


from rest_framework import viewsets


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)





# -------------------Using dataclasses.py----------------------

from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.dataclasses import SnippetData, UserData, serialize_snippet, serialize_user
from django.contrib.auth.models import User
from snippets.permissions import IsOwnerOrReadOnly

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def user_list(request):
    users = User.objects.all()
    user_data = [UserData.from_model(user, request) for user in users]
    return Response([serialize_user(user) for user in user_data])

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def snippet_list(request):
    snippets = Snippet.objects.all()
    snippet_data = [SnippetData.from_model(snippet, request) for snippet in snippets]
    return Response([serialize_snippet(snippet) for snippet in snippet_data])

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def snippet_create(request):
    data = {
        'title': request.data.get('title'),
        'code': request.data.get('code'),
        'linenos': request.data.get('linenos'),
        'language': request.data.get('language'),
        'style': request.data.get('style'),
    }
    
    # Create a new Snippet instance
    snippet = Snippet.objects.create(owner=request.user, **data)
    
    # Convert to SnippetData and return
    snippet_data = SnippetData.from_model(snippet, request)
    return Response(serialize_snippet(snippet_data), status=201)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def snippet_detail(request, pk):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=404)

    snippet_data = SnippetData.from_model(snippet, request)
    return Response(serialize_snippet(snippet_data))