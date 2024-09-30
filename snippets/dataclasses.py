# dataclasses.py

from dataclasses import dataclass, field
from typing import List

@dataclass
class SnippetData:
    url: str
    id: int
    highlight: str
    owner: str
    title: str
    code: str
    linenos: bool
    language: str
    style: str

    def to_dict(self):
        return {
            "url": self.url,
            "id": self.id,
            "highlight": self.highlight,
            "owner": self.owner,
            "title": self.title,
            "code": self.code,
            "linenos": self.linenos,
            "language": self.language,
            "style": self.style,
        }

@dataclass
class UserData:
    url: str
    id: int
    username: str
    snippets: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "url": self.url,
            "id": self.id,
            "username": self.username,
            "snippets": self.snippets,
        }
