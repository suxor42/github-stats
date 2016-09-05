import github
from datetime import date, datetime, timedelta
from json import dumps


def map_login_user(user_list):
    return list(map(github.get_user, user_list))


def cluster_on_date(commits, days_since):
    clusters = dict(zip(perdelta(date.today() - timedelta(days=days_since), date.today(), timedelta(days=1)), _set_gen()))
    for commit in commits:
        commit_date = datetime.strptime(commit.commit.committer.get('date'), '%Y-%m-%dT%H:%M:%SZ').date()
        if commit_date in clusters:
            if commit.author is not None:
                clusters[commit_date].add(commit.author.login)
    return clusters


def perdelta(start, end, delta):
    curr = start
    while curr <= end:
        yield curr
        curr += delta


def _list_gen():
    while True:
        yield list()


def _set_gen():
    while True:
        yield set()
