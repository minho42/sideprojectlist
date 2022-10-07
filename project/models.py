import os
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from sideprojectlist.models import TimeStampedModel
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from .tasks import save_info

# https://stackoverflow.com/questions/9522759/imagefield-overwrite-image-file-with-same-name
class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class Project(TimeStampedModel):
    slug = models.SlugField(max_length=100, allow_unicode=True)
    link = models.URLField(max_length=200, unique=True)
    maker_fullname = models.CharField(max_length=100)
    twitter_handle = models.CharField(max_length=20, null=True, blank=True, unique=True)
    twitter_followers_count = models.PositiveIntegerField(default=0)
    github_handle = models.CharField(max_length=20, null=True, blank=True, unique=True)
    is_approved = models.BooleanField(default=True)
    screenshot = models.ImageField(upload_to="screenshot/", null=True, blank=True, storage=OverwriteStorage)
    maker_avatar = models.ImageField(upload_to="avatar/", null=True, blank=True, storage=OverwriteStorage)
    tags = models.CharField(max_length=256, null=True, blank=True, help_text="Comma separated strings")
    cloudinary_screenshot_url = models.URLField(max_length=200, null=True, blank=True)
    cloudinary_maker_avatar_url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.maker_fullname}"

    def get_absolute_url(self):
        return reverse("project:list")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.maker_fullname)
        super().save(*args, **kwargs)

    class Meta:
        unique_together = [["link", "maker_fullname"]]

    @property
    def is_screenshot_not_saved(self):
        if self.screenshot and self.cloudinary_screenshot_url:
            return False
        return True

    @property
    def is_avatar_not_saved(self):
        if not self.twitter_handle:
            return False
        if self.maker_avatar and self.cloudinary_maker_avatar_url:
            return False
        return True

    @property
    def is_twitter_info_not_saved(self):
        return self.is_avatar_not_saved

    @property
    def tags_in_list(self):
        try:
            temp_tags = self.tags.strip().rstrip(",").split(",")
            return [tag.strip().lower() for tag in temp_tags]
        except AttributeError:
            return ""

    @property
    def like_count(self):
        return Like.objects.filter(project=self.id).count()

    @classmethod
    def screenshot_not_saved_count(cls):
        return Project.objects.filter(screenshot=None).count()

    @classmethod
    def users_without_screenshot(cls):
        return Project.objects.filter(cloudinary_screenshot_url__isnull=True)


# TODO check permission
@receiver(post_save, sender=Project)
# def project_post_save(sender, instance, created, **kwargs):
def project_post_save(sender, instance, created, raw, using, update_fields, **kwargs):
    if not created:
        return

    save_info.apply_async(
        args=(instance.id,),
        # link=success_callback.s(request.user.id),
        link=None,
        link_error=None,
    )


class Like(models.Model):
    project = models.ForeignKey(Project, related_name="liked_project", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="liked_user", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.project.maker_fullname} liked by {self.user}"
