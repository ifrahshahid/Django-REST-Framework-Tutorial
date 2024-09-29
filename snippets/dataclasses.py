# dataclasses.py
from dataclasses import dataclass, asdict, field
from django.urls import reverse
from snippets.models import Snippet
from django.contrib.auth.models import User

@dataclass
class SnippetData:
    id: int
    title: str
    code: str
    linenos: bool
    language: str
    style: str
    owner: str
    url: str = field(init=False)  
    highlight: str = field(init=False)  

    @staticmethod
    def from_model(snippet: Snippet, request) -> 'SnippetData':
        instance = SnippetData(
            id=snippet.id,
            title=snippet.title,
            code=snippet.code,
            linenos=snippet.linenos,
            language=snippet.language,
            style=snippet.style,
            owner=snippet.owner.username,
        )
        instance.url = request.build_absolute_uri(reverse('snippet-detail', args=[snippet.id]))
        instance.highlight = request.build_absolute_uri(reverse('snippet-highlight', args=[snippet.id]))
        return instance

@dataclass
class UserData:
    id: int
    username: str
    url: str = field(init=False)  
    snippets: list = field(default_factory=list)

    @staticmethod
    def from_model(user: User, request) -> 'UserData':
        instance = UserData(
            id=user.id,
            username=user.username
        )
        instance.url = request.build_absolute_uri(reverse('user-detail', args=[user.id]))
        return instance

#Create a method to serialize to dict
def serialize_snippet(snippet_data: SnippetData) -> dict:
    return asdict(snippet_data)

def serialize_user(user_data: UserData) -> dict:
    return asdict(user_data)
