from github3 import login
from datetime import datetime, timedelta
import os

USERNAME = os.environ.get('USERNAME')
TOKEN = os.environ.get('TOKEN')

GH = login(username=USERNAME, token=TOKEN)


def with_organization(function):
    def return_function(organization):
        org = filter(lambda org: org.login == organization, GH.iter_orgs()).__next__()
        return function(org)

    return return_function


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


@with_organization
def get_members(organization):
    return list(map(lambda member: member.login, organization.iter_members()))


@with_organization
def get_repos(organization):
    return list(map(lambda repo: repo.name, organization.iter_repos()))



