from rest_framework import serializers
from .models import Folder, Tag, Snippet


class FolderSerializer(serializers.ModelSerializer):
    """
    Serializer for Folders. Includes computed snippet count.
    """
    snippet_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Folder
        fields = ['id', 'name', 'color_accent', 'snippet_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'snippet_count']


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tags. Includes computed snippet count.
    """
    snippet_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'snippet_count', 'created_at']
        read_only_fields = ['id', 'created_at', 'snippet_count']


class SnippetSerializer(serializers.ModelSerializer):
    """
    Full serializer for Snippet CRUD.
    Supports reading nested tags and folders, and writing tags by name list.
    """
    folder_detail = FolderSerializer(source='folder', read_only=True)
    tags_detail = TagSerializer(source='tags', many=True, read_only=True)
    tag_names = serializers.ListField(
        child=serializers.CharField(max_length=50),
        write_only=True,
        required=False
    )

    class Meta:
        model = Snippet
        fields = [
            'id',
            'title',
            'description',
            'code',
            'language',
            'folder',
            'folder_detail',
            'tags_detail',
            'tag_names',
            'is_favorite',
            'is_public',
            'revision',
            'ai_summary',
            'ai_explanation',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'revision', 'created_at', 'updated_at']

    def validate_folder(self, value):
        """Ensure the folder belongs to the requesting user if authenticated."""
        if value is not None:
            user = self.context['request'].user
            if user.is_authenticated and value.user != user:
                raise serializers.ValidationError("You do not own this folder.")
        return value

    def _sync_tags(self, snippet, tag_names, user):
        """Associate tags with snippet, creating any new tags on the fly."""
        if tag_names is not None:
            tag_objects = []
            for name in tag_names:
                clean_name = name.strip().lower()
                if clean_name:
                    tag_obj, _ = Tag.objects.get_or_create(user=user, name=clean_name)
                    tag_objects.append(tag_obj)
            snippet.tags.set(tag_objects)

    def create(self, validated_data):
        tag_names = validated_data.pop('tag_names', None)
        user = validated_data.pop('user', None) or self.context['request'].user
        if not user or not user.is_authenticated:
            from django.contrib.auth.models import User
            user = User.objects.filter(username='ishan').first() or User.objects.first()
        snippet = Snippet.objects.create(user=user, **validated_data)
        self._sync_tags(snippet, tag_names, user)
        return snippet

    def update(self, instance, validated_data):
        tag_names = validated_data.pop('tag_names', None)
        user = validated_data.pop('user', None) or self.context['request'].user
        if not user or not user.is_authenticated:
            from django.contrib.auth.models import User
            user = User.objects.filter(username='ishan').first() or User.objects.first()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tag_names is not None:
            self._sync_tags(instance, tag_names, user)
        return instance


class SnippetListSerializer(serializers.ModelSerializer):
    """
    Optimized serializer for list views & dashboard cards. Includes full code for instant loading.
    """
    folder_detail = FolderSerializer(source='folder', read_only=True)
    tags_detail = TagSerializer(source='tags', many=True, read_only=True)
    preview = serializers.SerializerMethodField()

    class Meta:
        model = Snippet
        fields = [
            'id',
            'title',
            'description',
            'code',
            'language',
            'preview',
            'folder_detail',
            'tags_detail',
            'is_favorite',
            'is_public',
            'revision',
            'ai_summary',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'revision', 'created_at', 'updated_at']

    def get_preview(self, obj):
        """Return first 4 lines of code for snippet card preview."""
        lines = obj.code.splitlines()[:4]
        return '\n'.join(lines)
