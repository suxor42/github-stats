from flask import Flask
from flask import render_template
from flask_cache import Cache
from helper import map_login_user, cluster_on_date
import github
import os

OWNER = os.environ.get('GITHUB_REPO_OWNER')
REPOSITORY = os.environ.get('GITHUB_REPO')
ANDROID_DEV_GITHUB_NAMES = (os.environ.get('GITHUB_USERS')).split(' ')
ANDROID_DEV_GITHUB_USERS = None

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'
app.cache = Cache(app)


@app.route('/')
def hello_world():
    global ANDROID_DEV_GITHUB_USERS
    global OWNER
    global REPOSITORY
    global ANDROID_DEV_GITHUB_NAMES

    if ANDROID_DEV_GITHUB_USERS is None:
        ANDROID_DEV_GITHUB_USERS = map_login_user(ANDROID_DEV_GITHUB_NAMES)

    assert OWNER is not None
    assert REPOSITORY is not None
    assert ANDROID_DEV_GITHUB_USERS is not None
    assert len(ANDROID_DEV_GITHUB_USERS) > 0

    commits = github.get_commits(OWNER, REPOSITORY, 'master', 7)
    committer_clusters = cluster_on_date(commits, 7)
    return render_template(
        'commits.jinja2',
        user_list=ANDROID_DEV_GITHUB_USERS,
        commit_clusters=committer_clusters,
        owner=OWNER,
        repository=REPOSITORY
    )


if __name__ == '__main__':
    app.run()
