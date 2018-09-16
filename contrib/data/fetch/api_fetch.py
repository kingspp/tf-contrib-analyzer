# -*- coding: utf-8 -*-
"""
| **@created on:** 11/09/18,
| **@author:** prathyushsp,
| **@version:** v0.0.1
|
| **Description:**
| 
|
| **Sphinx Documentation Status:** --
|
"""

import glob
import json
import re
import base64
import networkx as nx
import matplotlib.pyplot as plt
from munch import Munch

# import requests

# BASE_DIR = '/Users/prathyushsp/Development/tf-contrib-analysis/contrib_usage_files/tf.contrib'


#
# file = json.load(open(files[0]))
#
# code = "Vae.Phenomenan of a unrelated nuclear flux, assimilate the life!\n\
# Selfs, followers, and eternal moons will always protect them.\n\
# Simmer minced broccolis in a basin with whiskey for about an hour to bring down their tartness.\n\
# import tensorflow as tf\n\
# # xyz = tf.contrib.layers.xavier()\n\
#  xyz = tf.contrib.layers.xavier()\n\
# Lads stutter with courage!\n\
# import tensorflow.contrib\
# from tensorflow import contrib\n\
# Dozens of space suits assimilate lunar, united spaces."
#
# # normal_usage = re.compile('tf\.contrib.*\(')
# normal_usage = re.compile('tf\.contrib\.[^\(|^\s]*')
# #
# commented_usage = re.compile('#.*(tf\.contrib[^\(]*)')
# import_usage = re.compile('import\ tensorflow\.contrib.*')
# commented_import_usage = re.compile('#.*(import\ tensorflow.contrib.*)')
# from_import_usage = re.compile('from\ tensorflow import contrib.*')
# commented_from_import_usage = re.compile('#.*(from\ tensorflow import contrib.*)')
#
# commented_lines = {}
# normal_lines = {}
#
# normal_lines_dag = nx.MultiDiGraph()
# # tf.contrib.framework.get_variables_by_name
#
# for file in files:
#     for item in json.load(open(file))['items']:
#         lines = base64.b64decode(item['content']['content']).decode('utf-8').split('\n')
#
#         for ln, line in enumerate(lines):
#             cu = commented_usage.findall(line)
#             nu = normal_usage.findall(line)
#             if cu:
#                 commented_lines[ln] = cu
#             elif nu:
#                 normal_lines[ln] = nu
#                 for nl in nu:
#                     nz = nl.split('.')
#                     for e, n in enumerate(nz):
#                         if e == 0:
#                             normal_lines_dag.add_node(n)
#                         else:
#                             normal_lines_dag.add_node(n)
#                             normal_lines_dag.add_edge(nz[e - 1], n)
# print(nx.layout)
# nx.draw_networkx(normal_lines_dag, pos=nx.spring_layout(normal_lines_dag, k=2))
# print(normal_lines_dag.nodes)
# plt.show()
# exit()
# exit()

# print(commented_lines)
# print('\n\n')
# print(normal_lines)


# class Api(object):
#     def __init__(self, name):
#         self.name = name
#         self.repo = None
#         self.repo_url = None
#         self.content = None
#         self.repo_stars = None
#         self.repo_watch = None


# class Repo(Munch):
#     def __init__(self, name, url, created_on, last_updated_on,
#                  home_page, owner, stars, watchers, language, forks,
#                  open_issues, search_store, search_topic):
#         super().__init__()
#         self.name = name
#         self.url = url
#         self.created_on = created_on
#         self.last_updated_on = last_updated_on
#         self.owner = owner
#         self.home_page = home_page
#         self.star_gazers = stars
#         self.watchers = watchers
#         self.language = language
#         self.forks = forks
#         self.open_issues = open_issues
#         self.search_score = search_store
#         self.search_topic = search_topic

from pymongo import MongoClient

client = MongoClient()

# Insert Repos

# BASE_DIR = '/Users/prathyushsp/Development/tf-contrib-analysis/repos'

# files = glob.glob(BASE_DIR + '/*/*.json')

# db = client.tf_contrib
# repos = db.repos

# for file in files:
#     d = json.load(open(file))
#     for item in d['items']:
#         item['topic'] = file.split('/')[-2]
#         r = repos.insert_one(item)
#     print(file)

# Insert Queries

# BASE_DIR = '/Users/prathyushsp/Development/tf-contrib-analysis/contrib_usage_files/tf.contrib'
# files = glob.glob(BASE_DIR + '/*.json')
#
#
# db = client.tf_contrib
# queries = db.queries
# for file in files:
#     d = json.load(open(file))
#     for item in d['items']:
#         item['query'] = 'tf.contrib'
#         r = queries.insert_one(item)
#     print(file)


# Create Usage Stats

from munch import Munch
import enum
from dataclasses import dataclass


#
# @dataclass
# class Record(Munch):
#     repo_name: str
#     line_no: int
#     usage_type: str
#     api_search_score: float
#     topic_search_score: float
#     api_query: str
#     topic_query: str
#     forks: int
#     watchers: int
#     stars: int
#     created_on: str
#     updated_on: str
#     pushed_on: str
#     file_url: str
#     path: str
#     size: int
#     owner: str
#     language: str
#     open_issues: int
#     api: str
#
#
# class UsageType(enum.Enum):
#     Normal = enum.auto()
#     Commented = enum.auto()
#
#
# BASE_DIR = '/Users/prathyushsp/Development/tf-contrib-analysis/contrib_usage_files/tf.contrib'
# files = glob.glob(BASE_DIR + '/*.json')
#
# normal_usage = re.compile('tf\.contrib\.[^\(|^\s]*')
# commented_usage = re.compile('#.*(tf\.contrib[^\(|^\s]*)')
#
# API_USAGE = {}
#
# repos = client.tf_contrib.repos
# queries = client.tf_contrib.queries
#
#
# def usage(api, line_no, repo_name, usage_type):
#     repo_details = repos.find_one({"full_name": repo_name})
#     query_details = queries.find_one({"repository.full_name": repo_name})
#
#     r = Record(repo_name=repo_name, line_no=line_no, usage_type=usage_type.name,
#                topic_search_score=repo_details['score'], api_search_score=query_details['score'],
#                file_url=query_details['html_url'], api_query='tf.contrib', topic_query=repo_details['topic'],
#                forks=repo_details['forks'], watchers=repo_details['watchers'], stars=repo_details['stargazers_count'],
#                size=repo_details['size'], created_on=repo_details['created_at'], pushed_on=repo_details['pushed_at'],
#                updated_on=repo_details['updated_at'], owner=repo_name.split('/')[0], language=repo_details['language'],
#                open_issues=repo_details['open_issues'], path=query_details['path'], api=api)
#     print(r['watchers'], r['stars'])
#     if api in API_USAGE:
#         API_USAGE[api].append(r)
#     else:
#         API_USAGE[api] = [r]
#
#
# db = client.tf_contrib
#
# for file in files:
#     d = json.load(open(file))
#     for item in d['items']:
#         lines = base64.b64decode(item['content']['content']).decode('utf-8').split('\n')
#         for l_no, line in enumerate(lines):
#             c_usage = commented_usage.findall(line)
#             if c_usage:
#                 usage(c_usage[0], l_no, item['repository']['full_name'], UsageType.Commented)
#             n_usage = normal_usage.findall(line)
#             if n_usage:
#                 usage(n_usage[0], l_no, item['repository']['full_name'], UsageType.Normal)


# Run Analysis on Usage Stats
usage = json.load(open('/tmp/usage.json'))


@dataclass
class UsageStats(Munch):
    id:int
    api: str
    total_usage: int
    total_stars: int
    # total_watchers: int
    total_fork: int
    total_issues: int
    # last_updated: str


stats = []
json_stats = []
for k, records in usage.items():
    _stars, _watchers, _forks, _issues, = 0, 0, 0, 0
    for record in records:
        _stars += record['stars']
        # _watchers += record['watchers']
        _forks += record['forks']
        _issues += record['open_issues']
    stats.append(
        UsageStats(id=k,api=k, total_usage=len(records), total_stars=_stars, total_fork=_forks,
                   total_issues=_issues))
    json_stats.append([k, len(records), _stars, _forks, _issues])



json.dump(stats, open('/tmp/stats.json', 'w'))
json.dump(json_stats, open('/tmp/json_stats.json', 'w'))
