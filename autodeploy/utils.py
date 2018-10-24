from django.conf import settings
from datetime import date
import os

celery_module = getattr(settings, 'AUTODEPLOY_CELERY', False)
celery = None
celery_schedule = None

if celery_module != False:
    module = __import__(celery_module, globals(), locals(), ['app'])
    celery = getattr(module, 'app')
    celery_schedule = getattr(settings, 'AUTODEPLOY_CELERY_SCHEDULE', False)

venv_python = getattr(settings, 'AUTODEPLOY_VENV_PYTHON', settings.BASE_DIR + '/venv')
work_tree = getattr(settings, 'AUTODEPLOY_WORK_TREE', settings.BASE_DIR)
git_dir = getattr(settings, 'AUTODEPLOY_DIR', settings.BASE_DIR + '/.git')
remote = getattr(settings, 'AUTODEPLOY_REMOTE', 'origin')
branch = getattr(settings, 'AUTODEPLOY_BRANCH', 'master')

uwsgi_filereload = getattr(settings, 'AUTODEPLOY_UWSGI_FILERELOAD', settings.BASE_DIR + '/restart')


def pull():
    os.system('git --work-tree=%s --git-dir=%s fetch --all' % (work_tree, git_dir))
    os.system('git --work-tree=%s --git-dir=%s checkout --force %s/%s' % (work_tree, git_dir, remote, branch))


def merge():
    os.system('%s %s/manage.py makemigrations --merge --noinput' % (venv_python, settings.BASE_DIR))


def migrate():
    os.system('%s %s/manage.py migrate --noinput' % (venv_python, settings.BASE_DIR))


def collectstatic():
    os.system('%s %s/manage.py collectstatic --noinput' % (venv_python, settings.BASE_DIR))


def uwsgi_reload():
    with open(uwsgi_filereload, 'w') as f:
        f.write(str(date.today()))
        f.close()


def add_release():
    if celery and not celery_schedule:
        release.delay()
    elif not celery:
        release()


def release():
    pull()
    merge()
    migrate()
    collectstatic()
    uwsgi_reload()


if celery_schedule:
    @celery.on_after_configure.connect
    def setup_periodic_tasks(sender, **kwargs):
        sender.add_periodic_task(celery_schedule, release(), name='autodeploy release')
