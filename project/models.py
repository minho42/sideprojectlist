from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from sideprojectlist.models import TimeStampedModel


class Project(TimeStampedModel):
    slug = models.SlugField(max_length=100, allow_unicode=True)
    link = models.URLField(max_length=200)
    maker_fullname = models.CharField(max_length=100)
    twitter_handle = models.CharField(max_length=20)
    github_handle = models.CharField(max_length=20)
    producthunt_handle = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=True)
    # description
    # category dev/design/...
    # avatar
    # description
    # owner

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
        import random

        return random.randint(0, 200)


class Upvote(models.Model):
    project = models.ForeignKey(
        Project, related_name="upvoted_project", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        Project, related_name="from_user", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
