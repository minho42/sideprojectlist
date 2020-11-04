from django import template
from project.models import Upvote

register = template.Library()


@register.filter("is_upvoted_by_me")
def is_upvoted_by_me(project, me):
    if not me.is_authenticated:
        return False
    return Upvote.objects.filter(project=project).filter(user=me).exists()
