from django.contrib import admin
from .models import Snippet

@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner')  # Customize this based on your needs
    search_fields = ('title', 'code')  # Allow searching by title or code
