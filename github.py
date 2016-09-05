from github3 import login
from datetime import datetime, timedelta
import os

USERNAME = os.environ.get('USERNAME')
TOKEN = os.environ.get('TOKEN')

GH = login(username=USERNAME, token=TOKEN)


def get_commits(owner, repository, branch='master', days_since=7):
    repo = GH.repository(owner=owner, repository=repository)
    return repo.iter_commits(sha=branch, since=(datetime.today() - timedelta(days=days_since)))


def get_contributors(owner, repository):
    repo = GH.repository(owner=owner, repository=repository)
    return [r.refresh() for r in repo.iter_contributors()]


def get_user(login):
    return GH.user(login=login)


def search_user(email):
    search_result = list(GH.search_users(query=email, number=1))
    if len(search_result) > 0:
        return search_result.pop()


def get_members(organization):
    org = filter(lambda org: org.login == organization, GH.iter_orgs()).__next__()
    return list(map(lambda member: member.login, org.iter_members()))
