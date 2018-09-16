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

dev_token = 'cb375cb020633787c748fc2f0ecedc85df542e68'
BASE_DIR = '/Users/prathyushsp/Development/tf-contrib-analysis/'

topics = ['neural-nets', 'tensorflow', 'machine-learning', 'neural-networks', 'deeplearning', 'deep-learning',
          'tensorflow-contrib', 'distributed_training', 'artificial-intelligence', 'ai', 'tf']

API_BASE = 'https://api.github.com/search/repositories?q=topic:{}+language:python+stars:>=10&page={}&per_page=100&access_token=cb375cb020633787c748fc2f0ecedc85df542e68'

for topic in topics:
    os.system('mkdir -p {}/{}'.format(BASE_DIR, topic))
    page_counter = 0
    while True:
        rd = requests.get(API_BASE.format('tensorflow', page_counter)).json()
        time.sleep(3)
        if 'incomplete_results' in rd:
            if rd['incomplete_results']:
                break
        else:
            break
        json.dump(rd, open(BASE_DIR + '/{}/{}.json'.format(topic, page_counter), 'w'))
        print('Working on {} : {}'.format(topic, page_counter))
        page_counter += 1
