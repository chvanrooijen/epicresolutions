from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import IntegrityError
from django.utils.text import slugify
from posts.models import Post

class Command(BaseCommand):
    help = 'Ensures all posts have unique slugs that conform to the expected pattern'

    def handle(self, *args, **kwargs):
        for post in Post.objects.all():
            with transaction.atomic():
                if not post.slug or Post.objects.filter(slug=post.slug).exclude(id=post.id).exists():
                    original_slug = slugify(post.title)
                    unique_slug = original_slug
                    num = 1
                    while Post.objects.filter(slug=unique_slug).exclude(id=post.id).exists():
                        unique_slug = f'{original_slug}-{num}'
                        num += 1
                    post.slug = unique_slug
                    try:
                        post.save()
                        self.stdout.write(self.style.SUCCESS(f'Successfully updated slug for post {post.id}'))
                    except IntegrityError:
                        self.stdout.write(self.style.ERROR(f'Failed to update slug for post {post.id} due to a unique constraint violation.'))