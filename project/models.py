from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from sideprojectlist.models import TimeStampedModel
from django.conf import settings


class Project(TimeStampedModel):
    slug = models.SlugField(max_length=100, allow_unicode=True)
    link = models.URLField(max_length=200)
    maker_fullname = models.CharField(max_length=100)
    twitter_handle = models.CharField(max_length=20, null=True, blank=True)
    github_handle = models.CharField(max_length=20, null=True, blank=True)
    producthunt_handle = models.CharField(max_length=20, null=True, blank=True)
    is_approved = models.BooleanField(default=True)
    description = models.TextField(max_length=256, null=True, blank=True)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # thumbnail = models.ImageField()
    # category dev/design/...

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