#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Nicolas Karolak'
SITENAME = 'Nicolas Karolak'
SITEURL = 'https://blog.karolak.fr'

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'fr'

# Feed generation is usually not desired when developing
FEED_ATOM = None
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TAG_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None

SOCIAL = (
    ('Blog', '#'),
    ('GitHub', '#'),
    ('SourceHut', '#'),
    )

DEFAULT_PAGINATION = 10
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
    )

AUTHORS_SAVE_AS = 'authors/index.html'
AUTHORS_URL = 'authors/'

ARCHIVES_SAVE_AS = 'archive/index.html'
ARCHIVES_URL = 'archive/'

ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'

DRAFT_SAVE_AS = 'drafts/{slug}/index.html'
DRAFT_URL = 'drafts/{slug}/'

CATEGORIES_SAVE_AS = 'category/index.html'
CATEGORIES_URL = 'category/'

CATEGORY_SAVE_AS = 'category/{slug}/index.html'
CATEGORY_URL = 'category/{slug}/'

PAGE_SAVE_AS = '{slug}/index.html'
PAGE_URL = '{slug}/'

TAG_SAVE_AS = 'tag/{slug}/index.html'
TAG_URL = 'tag/{slug}/'

TAGS_SAVE_AS = 'tag/index.html'
TAGS_URL = 'tag/'

YEAR_ARCHIVE_SAVE_AS = 'archive/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'archive/{date:%Y}/{date:%m}/index.html'
DAY_ARCHIVE_SAVE_AS = 'archive/{date:%Y}/{date:%m}/{date:%d}/index.html'

RELATIVE_URLS = True

THEME = 'etchy'
THEME_STATIC_DIR = 'static'

FAVICON = 'favicon.png'

STATIC_PATHS = [
    'static/robots.txt',
    'static/favicon.png',
    ]
EXTRA_PATH_METADATA = {
    'static/robots.txt': {'path': 'robots.txt'},
    'static/favicon.png': {'path': 'favicon.png'},
    }

MENUS = (
    ('/archive/', 'archives'),
    ('/category/', 'categories'),
    ('/tag/', 'tags'),
    ('/about/', 'about'),
    )

COMMENT_MAILINGLIST = '~nka/blog@lists.sr.ht'
COMMENT_MAILINGLIST_URL = 'https://lists.sr.ht/~nka/blog'

# disable syntax highlighting
MARKDOWN = {
    'extensions': ['extra', 'abbr'],
    }
