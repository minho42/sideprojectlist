from typing import Union
import environ
import tweepy
from tweepy.error import TweepError
from core.utils import save_image_from_url
from django.apps import apps
from django.shortcuts import get_object_or_404

env = environ.Env()
environ.Env.read_env()


class TwitterSaver:
    def __init__(self):
        self.api = self._get_api()

    def _get_api(self) -> object:
        auth = tweepy.OAuthHandler(
            env("TWITTER_CONSUMER_KEY"), env("TWITTER_CONSUMER_SECRET")
        )
        auth.set_access_token(
            env("TWITTER_ACCESS_TOKEN"),
            env("TWITTER_ACCESS_TOKEN_SECRET"),
        )

        api = tweepy.API(auth)
        # TODO catch potential exception
        return api

    def _get_user(self, handle: str) -> Union[object, None]:
        try:
            user = self.api.get_user(handle)
        except TweepError:
            print(f"handle: {handle}")
            user = None
        return user

    def _get_bio(self, handle: str) -> Union[str, None]:
        user = self._get_user(handle)
        if not user:
            return
        return user.description

    def _get_profile_image_url(self, handle: str) -> Union[str, None]:
        user = self._get_user(handle)
        if not user:
            return
        return user.profile_image_url_https

    def save_bio(self, project_id) -> None:
        Project = apps.get_model("project", "Project")
        p = get_object_or_404(Project, id=project_id)
        if not p.twitter_handle:
            return
        bio = self._get_bio(p.twitter_handle)
        if bio:
            p.maker_bio = bio
            p.save()

    def save_profile_image(self, project_id) -> None:
        Project = apps.get_model("project", "Project")
        p = get_object_or_404(Project, id=project_id)
        url = self._get_profile_image_url(p.twitter_handle)
        if url:
            save_image_from_url(p.maker_avatar, url)
