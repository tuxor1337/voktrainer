# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='Vokabeltrainer für Linux',
    version='1.0.1',
    description='Vokabeltrainer geschrieben in Python',
    url='https://framagit.org/tuxor1337/voktrainer',
    author='Thomas Vogt',
    author_email='thomas.vogt@tovotu.de',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Topic :: Education',
    ],
    keywords='Vokabeltrainer Sprachen flash-cards languages',
    packages=find_packages(),
    package_data={'': ['*.glade']},
    scripts=["bin/voktrainer"],
    data_files=[("share/applications",["setup_data/voktrainer.desktop"]),
                ("share/pixmaps",["setup_data/voktrainer.svg"])],
    project_urls={ 'Source': 'https://framagit.org/tuxor1337/voktrainer', },
)
