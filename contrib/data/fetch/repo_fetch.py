# -*- coding: utf-8 -*-
"""
| **@created on:** 10/09/18,
| **@author:** prathyushsp,
| **@version:** v0.0.1
|
| **Description:**
| 
|
| **Sphinx Documentation Status:** --
|
"""

import requests
import json
import os
import time

BASE_DIR = '/Users/prathyushsp/Development/tmp/tf-contrib-analysis/'

topics = ['neural-nets', 'tensorflow', 'machine-learning', 'neural-networks', 'deeplearning', 'deep-learning',
          'tensorflow-contrib', 'distributed_training', 'artificial-intelligence', 'ai', 'tf']

API_BASE = 'https://api.github.com/search/repositories?q=topic:{}+language:python+stars:>=10&page={}&per_page=100&access_token=46d36c4c99a9ae5ac14599308ddb4ac746cc8f58&'

from ratelimit import limits, sleep_and_retry


@sleep_and_retry
@limits(calls=29, period=60)
def query(url):
    return requests.get(url)


from pymongo import MongoClient

client = MongoClient()

db = client.tf_sunset
repos = db.repos

# for topic in topics:
#     os.system('mkdir -p {}/{}'.format(BASE_DIR, topic))
#     page_counter = 0
#     rd = query(API_BASE.format(topic, page_counter)).json()
#     while 'incomplete_results' in rd and not rd['incomplete_results']:
#         for item in rd['items']:
#             item['topic'] = topic
#             repos.insert_one(item)
#         print('Working on {} : {}'.format(topic, page_counter))
#         page_counter += 1
#         rd = query(API_BASE.format(topic, page_counter)).json()


# API_BASE = 'https://api.github.com/search/code?q=tensorflow.contrib+repo:{}&per_page=100&access_token=46d36c4c99a9ae5ac14599308ddb4ac746cc8f58'
#
# total_repos = repos.count()
queries = db.queries
#
# for f_no, repo in enumerate(db.repos.find()):
#     req = query(API_BASE.format(repo['full_name'])).json()
#     if 'total_count' in req and req['total_count'] == 0 or 'items' not in req:
#         continue
#     for e, item in enumerate(req['items']):
#         content = query(item['git_url'] + '?&access_token=').json()
#         req['items'][e]['content'] = content
#         req['items'][e]['query'] = 'tf.contrib'
#     queries.insert_many(req['items'])
#     print('Saving: {}. {} / {} '.format(repo['full_name'], f_no, total_repos))

from munch import Munch
import enum
from dataclasses import dataclass
import re
import base64


@dataclass
class Record(Munch):
    repo_name: str
    line_no: int
    usage_type: str
    api_search_score: float
    topic_search_score: float
    api_query: str
    topic_query: str
    forks: int
    watchers: int
    stars: int
    created_on: str
    updated_on: str
    pushed_on: str
    file_url: str
    path: str
    size: int
    owner: str
    language: str
    open_issues: int
    api: str


class UsageType(enum.Enum):
    Normal = enum.auto()
    Commented = enum.auto()


normal_usage = re.compile('tf\.contrib\.[^\(|^\s]*')
commented_usage = re.compile('#.*(tf\.contrib[^\(|^\s]*)')

API_USAGE = {}

def usage(api, line_no, repo_name, usage_type):
    repo_details = repos.find_one({"full_name": repo_name})
    query_details = queries.find_one({"repository.full_name": repo_name})
    r = Record(repo_name=repo_name, line_no=line_no, usage_type=usage_type.name,
               topic_search_score=repo_details['score'], api_search_score=query_details['score'],
               file_url=query_details['html_url'], api_query='tf.contrib', topic_query=repo_details['topic'],
               forks=repo_details['forks'], watchers=repo_details['watchers'], stars=repo_details['stargazers_count'],
               size=repo_details['size'], created_on=repo_details['created_at'], pushed_on=repo_details['pushed_at'],
               updated_on=repo_details['updated_at'], owner=repo_name.split('/')[0], language=repo_details['language'],
               open_issues=repo_details['open_issues'], path=query_details['path'], api=api)
    if api in API_USAGE:
        API_USAGE[api].append(r)
    else:
        API_USAGE[api] = [r]


for q_no, query in enumerate(queries.find()):
    lines = base64.b64decode(query['content']['content']).decode('utf-8').split('\n')
    for l_no, line in enumerate(lines):
        c_usage = commented_usage.findall(line)
        if c_usage:
            usage(c_usage[0], l_no, query['repository']['full_name'], UsageType.Commented)
            continue
        n_usage = normal_usage.findall(line)
        if n_usage:
            usage(n_usage[0], l_no, query['repository']['full_name'], UsageType.Normal)


@dataclass
class UsageStats(Munch):
    id:int
    api: str
    total_usage: int
    total_stars: int
    total_fork: int
    total_issues: int

stats = []

for k, records in API_USAGE.items():
    _stars, _watchers, _forks, _issues, = 0, 0, 0, 0
    for record in records:
        _stars += record['stars']
        _forks += record['forks']
        _issues += record['open_issues']
    stats.append(
        UsageStats(id=k,api=k, total_usage=len(records), total_stars=_stars, total_fork=_forks,
                   total_issues=_issues))

