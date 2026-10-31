import uuid
from django.contrib.auth.models import User
from django.db import models


class Folder(models.Model):
    """
    Folders allow users to organize snippets hierarchically.
    Each folder belongs to a specific user and has an accent color.
    """
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    color_accent = models.CharField(max_length=20, default='#3B82F6')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_user_folder')
        ]

    def __str__(self):
        return f"{self.user.username}/{self.name}"


class Tag(models.Model):
    """
    Tags provide flexible, multi-category labelling for snippets.
    Tags are unique per user.
    """
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')
    color = models.CharField(max_length=20, default='#10B981')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_user_tag')
        ]

    def __str__(self):
        return f"#{self.name}"


class Snippet(models.Model):
    """
    Core Code Snippet model.
    Stores code content, programming language, AI summaries/explanations,
    and references to folders and tags. Uses UUID for secure sharing and live room URLs.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='snippets')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    code = models.TextField()
    language = models.CharField(max_length=50, default='javascript', db_index=True)
    
    # Organization
    folder = models.ForeignKey(
        Folder, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='snippets'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='snippets')
    
    # Flags & Visibility
    is_favorite = models.BooleanField(default=False, db_index=True)
    is_public = models.BooleanField(default=False, db_index=True)
    
    # AI Enhancements (Gemini Auto-Documenter)
    ai_summary = models.TextField(blank=True, null=True)
    ai_explanation = models.TextField(blank=True, null=True)
    
    # Concurrency & Revision Control (Phase 7 Single Source of Truth)
    revision = models.PositiveIntegerField(default=1, db_index=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.language})"
