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
from munch import Munch
import enum
from dataclasses import dataclass
import re
import base64
from requests.auth import HTTPBasicAuth
from pymongo import MongoClient
from ratelimit import limits, sleep_and_retry
import time

BASE_DIR = '/Users/prathyushsp/Development/tmp/tf-contrib-analysis_v1/'


@sleep_and_retry
@limits(calls=29, period=60)
def query(url):
    return requests.get(url)


client = MongoClient()

db = client.tf_contrib
repos = db.repos


def fetch_repos():
    topics = ['neural-nets', 'tensorflow', 'machine-learning', 'neural-networks', 'deeplearning', 'deep-learning',
              'tensorflow-contrib', 'distributed_training', 'artificial-intelligence', 'ai', 'tf']
    API_BASE = 'https://api.github.com/search/repositories?q=topic:{}+language:python+stars:>=10&page={}&per_page=100'

    for topic in topics:
        print(f'Starting {topic} topic')
        page_counter = 0
        rd = query(API_BASE.format(topic, page_counter)).json()
        if 'message' in rd and rd['message'] == 'Bad credentials':
            raise Exception('Bad Credentials')
        while 'incomplete_results' in rd and not rd['incomplete_results']:
            for item in rd['items']:
                item['topic'] = topic
                repos.insert_one(item)
            print('Working on {} : {}'.format(topic, page_counter))
            page_counter += 1
            rd = query(API_BASE.format(topic, page_counter)).json()
    print('Finding repos completed successfully . . .')


def fetch_code():
    API_BASE = 'https://api.github.com/search/code?q=tensorflow.contrib+repo:{}&per_page=100'

    total_repos = repos.count()
    queries = db.queries
    cursor = db.repos.find(no_cursor_timeout=True)
    for f_no, repo in enumerate(cursor):
        req = query(API_BASE.format(repo['full_name'])).json()
        if 'total_count' in req and req['total_count'] == 0 or 'items' not in req:
            continue
        for e, item in enumerate(req['items']):
            content = query(item['git_url'] + '?').json()
            req['items'][e]['content'] = content
            req['items'][e]['query'] = 'tf.contrib'
        queries.insert_many(req['items'])
        print('Saving: {}. {} / {} '.format(repo['full_name'], f_no, total_repos))
    cursor.close()


def fetch_usage():
    queries = db.queries

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

    def usage(api, line_no, repo_name, usage_type, query_details):
        repo_details = repos.find_one({"full_name": repo_name})
        r = Record(repo_name=repo_name, line_no=line_no, usage_type=usage_type.name,
                   topic_search_score=repo_details['score'], api_search_score=query_details['score'],
                   file_url=query_details['html_url'], api_query='tf.contrib', topic_query=repo_details['topic'],
                   forks=repo_details['forks'], watchers=repo_details['watchers'],
                   stars=repo_details['stargazers_count'],
                   size=repo_details['size'], created_on=repo_details['created_at'],
                   pushed_on=repo_details['pushed_at'],
                   updated_on=repo_details['updated_at'], owner=repo_name.split('/')[0],
                   language=repo_details['language'],
                   open_issues=repo_details['open_issues'], path=query_details['path'], api=api)
        if api in API_USAGE:
            API_USAGE[api].append(r)
        else:
            API_USAGE[api] = [r]

    for q_no, query in enumerate(queries.find()):
        if 'content' in query and 'content' in query['content']:
            lines = base64.b64decode(query['content']['content']).decode('utf-8').split('\n')
            for l_no, line in enumerate(lines):
                n_usage = normal_usage.findall(line)
                if n_usage:
                    usage(n_usage[0], l_no + 1, query['repository']['full_name'], UsageType.Normal, query)
        else:
            print(f'Skipping {query["path"]}')
    json.dump(API_USAGE, open('/tmp/api_usage.json', 'w'))


def create_stats():
    API_USAGE = json.load(open('/tmp/api_usage.json'))

    @dataclass
    class UsageStats(Munch):
        id: int
        api: str
        total_usage: int
        total_stars: int
        total_fork: int
        total_issues: int
        created_on: str
        updated_on: str

    stats = []
    _lines = []
    for k, records in API_USAGE.items():
        _stars, _watchers, _forks, _issues, = 0, 0, 0, 0
        _created_on, _last_updated_on = [], []
        for record in records:
            _stars += record['stars']
            _forks += record['forks']
            _issues += record['open_issues']
            _created_on.append(record['created_on'])
            _last_updated_on.append(record['updated_on'])
            _lines.append(record['repo_name'])

        stats.append(
            UsageStats(id=k, api=k, total_usage=len(records), total_stars=_stars, total_fork=_forks,
                       total_issues=_issues, updated_on=sorted(_last_updated_on)[-1],
                       created_on=sorted(_created_on)[0]))

    json.dump({"timestamp": int(time.time()),
               "total_api": len(stats),
               "total_lines": len(_lines),
               "total_projects": len(set(_lines)),
               "data": stats}, open('/Users/prathyushsp/Git/tf-contrib-analyzer/static/data/stats_v1.json', 'w'))


if __name__ == '__main__':
    fetch_repos()
    fetch_code()
    fetch_usage()
    create_stats()
