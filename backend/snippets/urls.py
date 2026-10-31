from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SnippetViewSet, FolderViewSet, TagViewSet

app_name = 'snippets'

router = DefaultRouter()
router.register(r'snippets', SnippetViewSet, basename='snippet')
router.register(r'folders', FolderViewSet, basename='folder')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
]
