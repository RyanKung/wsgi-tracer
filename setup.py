import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


install_requires = [
    line
    for line in open(
        os.path.join(here, "requirements.txt"),
        "r"
    )
]
author = 'Ryan Kung'
email = 'ryankung@ieee.org'


setup(
    name='wsgi_tracer',
    description='wsgi_tracer is a APM tracer helper for gunicorn',
    version='1.4',
    packages=find_packages(here, exclude=['tests']),
    license='GPL',
    author=author,
    author_email=email,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
