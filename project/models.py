from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from sideprojectlist.models import TimeStampedModel

from .tasks import save_info


class Project(TimeStampedModel):
    slug = models.SlugField(max_length=100, allow_unicode=True)
    link = models.URLField(max_length=200)
    maker_fullname = models.CharField(max_length=100)
    maker_bio = models.TextField(max_length=256, null=True, blank=True)
    twitter_handle = models.CharField(max_length=20, null=True, blank=True)
    github_handle = models.CharField(max_length=20, null=True, blank=True)
    producthunt_handle = models.CharField(max_length=20, null=True, blank=True)
    is_approved = models.BooleanField(default=True)
    screenshot = models.ImageField(upload_to="screenshot/", null=True, blank=True)
    maker_avatar = models.ImageField(upload_to="avatar/", null=True, blank=True)
    tags = models.CharField(
        max_length=256, null=True, blank=True, help_text="Comma separated strings"
    )
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
    def tags_in_list(self):
        try:
            return self.tags.rstrip(",").split(",")
        except AttributeError:
            return ""

    @property
    def like_count(self):
        return Like.objects.filter(project=self.id).count()


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
    project = models.ForeignKey(
        Project, related_name="liked_project", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="liked_user", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.project.maker_fullname} liked by {self.user}"