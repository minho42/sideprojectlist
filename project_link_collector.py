import requests
from requests.exceptions import MissingSchema
from lxml import html

s = requests.session()


def trim_trailing_slash(path: str) -> str:
    if path.endswith("/"):
        path = path[:-1]
    return path


def is_there_projects(url):
    url = trim_trailing_slash(url)
    urls_to_try = [
        f"{url}/project",
        f"{url}/projects",
    ]
    for u in urls_to_try:
        try:
            r = s.get(u)
            if str(r.status_code).startswith("2"):
                return u
        except MissingSchema:
            pass
    return False


starting_url = "https://chriscoyier.net/"

r = s.get(starting_url)
node = html.fromstring(r.content)
links = node.xpath("//a/@href")
project_links = []
for link in links:
    is_link = is_there_projects(link)
    if is_link:
        if is_link not in project_links:
            project_links.append(is_link)
            print(is_link)