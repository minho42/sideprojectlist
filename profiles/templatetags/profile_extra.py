from django import template

register = template.Library()


@register.inclusion_tag("profiles/profile_card.html", takes_context=True)
def profile_card(context, profile_user):
    request = context.get("request")
    current_user = request.user
    # TODO Make names clear
    return {"user": current_user, "u": profile_user}
