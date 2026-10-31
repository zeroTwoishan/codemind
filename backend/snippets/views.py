from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import Folder, Tag, Snippet
from .serializers import (
    FolderSerializer,
    TagSerializer,
    SnippetSerializer,
    SnippetListSerializer,
)
from .ai_services import enhance_code_snippet

User = get_user_model()


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_root_view(request):
    """
    Welcoming API Root endpoint giving directory and status metadata.
    """
    return Response({
        'name': 'CodeMind Vault API',
        'version': '1.0.0',
        'status': 'online',
        'endpoints': {
            'auth_register': '/api/auth/register/',
            'auth_token': '/api/auth/token/',
            'auth_refresh': '/api/auth/token/refresh/',
            'auth_me': '/api/auth/me/',
            'snippets': '/api/snippets/',
            'ai_enhance': '/api/snippets/ai-enhance/',
            'folders': '/api/folders/',
            'tags': '/api/tags/',
            'admin': '/admin/',
        },
        'docs': 'CodeMind AI Code Vault REST API Engine'
    })


class FolderViewSet(viewsets.ModelViewSet):
    """
    CRUD ViewSet for user folders with snippet count aggregation.
    """
    serializer_class = FolderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Folder.objects.annotate(
                snippet_count=Count('snippets', filter=Q(snippets__is_public=True), distinct=True)
            ).order_by('name')
        return Folder.objects.filter(
            user=self.request.user
        ).annotate(
            snippet_count=Count('snippets', distinct=True)
        ).order_by('name')

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            user = User.objects.filter(username='ishan').first() or User.objects.first()
        serializer.save(user=user)


class TagViewSet(viewsets.ModelViewSet):
    """
    CRUD ViewSet for user tags with snippet count aggregation.
    """
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Tag.objects.all().order_by('name')[:30]
        return Tag.objects.filter(
            user=self.request.user
        ).annotate(
            snippet_count=Count('snippets', distinct=True)
        ).order_by('name')

    def perform_create(self, serializer):
        name = serializer.validated_data.get('name', '').strip().lower()
        user = self.request.user
        if not user.is_authenticated:
            user = User.objects.filter(username='ishan').first() or User.objects.first()
        serializer.save(user=user, name=name)


class SnippetViewSet(viewsets.ModelViewSet):
    """
    Full CRUD ViewSet for Snippets with search, multi-tag filtering,
    language filtering, favorite toggle, and AI code enhancement.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return SnippetListSerializer
        return SnippetSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = Snippet.objects.filter(
                Q(user=user) | Q(is_public=True)
            ).select_related('folder', 'user').prefetch_related('tags').distinct()
        else:
            queryset = Snippet.objects.filter(
                is_public=True
            ).select_related('folder', 'user').prefetch_related('tags').distinct()

        # Filter by folder (supports ID or Name)
        folder_id = self.request.query_params.get('folder')
        if folder_id:
            if str(folder_id).lower() == 'uncategorized':
                queryset = queryset.filter(folder__isnull=True)
            elif str(folder_id).isdigit():
                queryset = queryset.filter(folder_id=int(folder_id))
            else:
                queryset = queryset.filter(folder__name__iexact=folder_id)

        # Filter by tag name or tag id
        tag = self.request.query_params.get('tag')
        if tag:
            if str(tag).isdigit():
                queryset = queryset.filter(tags__id=int(tag))
            else:
                queryset = queryset.filter(tags__name__iexact=tag)

        # Filter by language
        language = self.request.query_params.get('language')
        if language:
            queryset = queryset.filter(language__iexact=language)

        # Filter by favorites
        favorite = self.request.query_params.get('is_favorite')
        if favorite is not None:
            is_fav = favorite.lower() in ('true', '1')
            queryset = queryset.filter(is_favorite=is_fav)

        # Search query (matches title, description, code, ai_summary)
        search_query = self.request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(code__icontains=search_query) |
                Q(ai_summary__icontains=search_query)
            )

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            user = User.objects.filter(username='ishan').first() or User.objects.first()
        serializer.save(user=user)

    def update(self, request, *args, **kwargs):
        from .services import update_snippet_content, RevisionConflictError

        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        expected_revision = request.data.get('revision') or request.data.get('expected_revision')
        code = request.data.get('code')

        # If revision concurrency control is invoked or code is being updated
        if expected_revision is not None or code is not None:
            try:
                updated_snippet, _ = update_snippet_content(
                    snippet_id=instance.id,
                    code=code,
                    expected_revision=int(expected_revision) if expected_revision is not None else None,
                    user=request.user,
                    title=request.data.get('title'),
                    description=request.data.get('description'),
                    language=request.data.get('language'),
                )
                serializer = self.get_serializer(updated_snippet)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except RevisionConflictError as exc:
                return Response({
                    'error': 'Revision conflict',
                    'message': exc.message,
                    'current_revision': exc.current_revision,
                    'latest_code': exc.latest_code,
                }, status=status.HTTP_409_CONFLICT)

        return super().update(request, *args, partial=partial, **kwargs)

    @action(detail=True, methods=['post'], url_path='toggle-favorite')
    def toggle_favorite(self, request, pk=None):
        """
        Toggle the favorite state of a snippet.
        """
        snippet = self.get_object()
        snippet.is_favorite = not snippet.is_favorite
        snippet.save(update_fields=['is_favorite'])
        return Response({
            'id': str(snippet.id),
            'is_favorite': snippet.is_favorite,
            'message': f"Snippet {'marked as favorite' if snippet.is_favorite else 'removed from favorites'}."
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='ai-enhance', permission_classes=[permissions.AllowAny])
    def ai_enhance(self, request):
        """
        AI Auto-Documenter endpoint using Gemini 3.6 Flash.
        Accepts: { code: str, language: str (optional), instructions: str (optional), snippet_id: uuid (optional) }
        Returns: { improved_code, summary, explanation, suggested_tags, language, time_complexity, space_complexity }
        """
        code = request.data.get('code', '').strip()
        if not code:
            return Response(
                {'error': 'Code field is required.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        language = request.data.get('language', '')
        instructions = request.data.get('instructions', '')
        snippet_id = request.data.get('snippet_id')

        ai_result = enhance_code_snippet(
            code=code, 
            language=language, 
            instructions=instructions
        )

        response_data = ai_result.model_dump()

        # If a snippet_id was passed and user is authenticated, update that snippet's AI fields & tags
        if snippet_id and request.user and request.user.is_authenticated:
            try:
                snippet = Snippet.objects.get(id=snippet_id, user=request.user)
                snippet.ai_summary = ai_result.summary
                snippet.ai_explanation = ai_result.explanation
                if request.data.get('apply_code', False):
                    snippet.code = ai_result.improved_code
                snippet.save()
                
                # Auto-sync tags
                if ai_result.suggested_tags:
                    for tag_name in ai_result.suggested_tags:
                        clean_tag = tag_name.strip().lower()
                        if clean_tag:
                            tag_obj, _ = Tag.objects.get_or_create(user=request.user, name=clean_tag)
                            snippet.tags.add(tag_obj)

                response_data['snippet_updated'] = True
            except Snippet.DoesNotExist:
                pass

        return Response(response_data, status=status.HTTP_200_OK)
