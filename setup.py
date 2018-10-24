from setuptools import setup, find_packages

setup(
    name="AutoDeploy for Django",
    version=__import__("autodeploy").__version__,
    description="Автоматически подтягивает изменения из bitbucket, может работать с celery, celery beat",
    long_description=open('README.rst').read(),
    author="Krulikovskiy Nikita",
    author_email="it@krulikovskiy.com",
    url="https://github.com/krulikovskiy/django-autodeploy",
    packages=find_packages(),
    install_requires=[
        'django>=2.0',
    ],
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    zip_safe=False,
)
