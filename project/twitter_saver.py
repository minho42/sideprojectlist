import environ
import tweepy
from core.utils import save_image_from_url
from django.apps import apps
from django.shortcuts import get_object_or_404

env = environ.Env()
environ.Env.read_env()


class TwitterSaver:
    def __init__(self):
        self.api = self._get_api()

    def _get_api(self):
        auth = tweepy.OAuthHandler(
            env("TWITTER_CONSUMER_KEY"), env("TWITTER_CONSUMER_SECRET")
        )
        auth.set_access_token(
            env("TWITTER_ACCESS_TOKEN"),
            env("TWITTER_ACCESS_TOKEN_SECRET"),
        )

        api = tweepy.API(auth)
        return api

    def _get_bio(self, handle):
        return self.api.get_user(handle).description

    def _get_profile_image_url(self, handle):
        return self.api.get_user(handle).profile_image_url_https

    def save_bio(self, project_id):
        Project = apps.get_model("project", "Project")
        p = get_object_or_404(Project, id=project_id)
        bio = self._get_bio(p.twitter_handle)

    def save_profile_image(self, project_id):
        Project = apps.get_model("project", "Project")
        p = get_object_or_404(Project, id=project_id)
        url = self._get_profile_image_url(p.twitter_handle)
        save_image_from_url(p.maker_avatar, url)
