from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import Crop, ResizeToFill
from PIL import Image
from sideprojectlist.models import TimeStampedModel

from .tasks import save_screenshot


class Project(TimeStampedModel):
    slug = models.SlugField(max_length=100, allow_unicode=True)
    link = models.URLField(max_length=200)
    maker_fullname = models.CharField(max_length=100)
    maker_bio = models.TextField(max_length=256, null=True, blank=True)
    twitter_handle = models.CharField(max_length=20, null=True, blank=True)
    github_handle = models.CharField(max_length=20, null=True, blank=True)
    producthunt_handle = models.CharField(max_length=20, null=True, blank=True)
    is_approved = models.BooleanField(default=True)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    screenshot = models.ImageField(
        upload_to="screenshot/",
        null=True,
        blank=True
        # default="screenshot/default.png",
    )
    # https://django-imagekit.readthedocs.io
    # 2560
    screenshot_thumbnail = ImageSpecField(
        source="screenshot",
        processors=[Crop(2560, 5120)],
        format="JPEG",
        options={"quality": 60},
    )
    maker_avatar = models.ImageField(upload_to="avatar/", null=True, blank=True)
    maker_avatar_thumbnail = ImageSpecField(
        source="screenshot",
        processors=[ResizeToFill(30, 30)],
        format="JPEG",
        options={"quality": 80},
    )
    tags = models.CharField(
        max_length=256, null=True, blank=True, help_text="Comma separated strings"
    )

    def __str__(self):
        return f"{self.twitter_handle}: {self.link}"

    def get_absolute_url(self):
        return reverse("project:list")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.maker_fullname)
        super().save(*args, **kwargs)

    class Meta:
        unique_together = [["link", "maker_fullname"]]

    @property
    def upvote_count(self):
        return Upvote.objects.filter(project=self.id).count()

    @property
    def tags_in_list(self):
        try:
            return self.tags.rstrip(",").split(",")
        except AttributeError:
            return ""


@receiver(post_save, sender=Project)
def project_post_save(sender, instance, created, **kwargs):
    if not created:
        return

    save_screenshot.apply_async(
        args=(instance.id,),
        # link=success_callback.s(request.user.id),
        link=None,
        link_error=None,
    )


class Upvote(models.Model):
    project = models.ForeignKey(
        Project, related_name="upvoted_project", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="from_user", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.project.maker_fullname} - {self.user}"


class Comment(TimeStampedModel):
    pass
    # project
    # user
    # text
    # parent
