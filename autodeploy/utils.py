from django.conf import settings
from datetime import datetime
import subprocess

celery_module = getattr(settings, 'AUTODEPLOY_CELERY', False)
celery = None
celery_schedule = None

if celery_module != False:
    module = __import__(celery_module, globals(), locals(), ['app'])
    celery = getattr(module, 'app')
    celery_schedule = getattr(settings, 'AUTODEPLOY_CELERYBEAT_SCHEDULE', False)

venv_bin = getattr(settings, 'AUTODEPLOY_VENV_PYTHON', settings.BASE_DIR + '/venv/bin')
venv_python = venv_bin + '/python'
venv_pip = venv_bin + '/pip'

work_tree = getattr(settings, 'AUTODEPLOY_WORK_TREE', settings.BASE_DIR)
git_dir = getattr(settings, 'AUTODEPLOY_DIR', settings.BASE_DIR + '/.git')
remote = getattr(settings, 'AUTODEPLOY_REMOTE', 'origin')
branch = getattr(settings, 'AUTODEPLOY_BRANCH', 'master')

uwsgi_filereload = getattr(settings, 'AUTODEPLOY_UWSGI_FILERELOAD', settings.BASE_DIR + '/.restart')


def pull():
    subprocess.check_output('git --work-tree=%s --git-dir=%s fetch --all' % (work_tree, git_dir), shell=True)
    subprocess.check_output(
        'git --work-tree=%s --git-dir=%s checkout --force %s/%s' % (work_tree, git_dir, remote, branch), shell=True)


def requirements():
    subprocess.check_output('%s install -r %s/requirements.txt' % (venv_pip, settings.BASE_DIR), shell=True)


def merge():
    subprocess.check_output('%s %s/manage.py makemigrations --merge --noinput' % (venv_python, settings.BASE_DIR),
                            shell=True)


def migrate():
    subprocess.check_output('%s %s/manage.py migrate --noinput' % (venv_python, settings.BASE_DIR), shell=True)


def collectstatic():
    subprocess.check_output('%s %s/manage.py collectstatic --noinput' % (venv_python, settings.BASE_DIR), shell=True)


def uwsgi_reload():
    with open(uwsgi_filereload, 'w') as f:
        f.write(str(datetime.today()))
        f.close()


def commands():
    pull()
    requirements()
    merge()
    migrate()
    collectstatic()
    uwsgi_reload()


if celery:
    @celery.task
    def release():
        commands()
else:
    def release():
        commands()


def add_release():
    if celery and not celery_schedule:
        release.delay()
    elif not celery:
        release()


if celery_schedule:
    @celery.on_after_configure.connect
    def setup_periodic_tasks(sender, **kwargs):
        sender.add_periodic_task(celery_schedule, release(), name='autodeploy release')
