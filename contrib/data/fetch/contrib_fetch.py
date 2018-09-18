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

import glob
import json
import requests

REPO_FETCH_DIR = '/Users/prathyushsp/Development/tf-contrib-analysis/repos'
SAVE_DIR = '/Users/prathyushsp/Development/tf-contrib-analysis/contrib_usage_files/tensorflow.contrib/'
API_BASE = 'https://api.github.com/search/code?q=tensorflow.contrib+repo:{}&per_page=100&access_token=&'
files = glob.glob(REPO_FETCH_DIR + "/*/*.json")

lf = len(files)

repos = []
for fc, f in enumerate(files):
    for r_name in json.load(open(f))['items']:
        repos.append(r_name['full_name'])
        # print('Repository: {}'.format(r_name['full_name']))

repos = set(repos)
lf = len(repos)

from ast import literal_eval

# success_list = literal_eval(
#     open('/Users/prathyushsp/Development/tf-contrib-analysis/contrib_usage_files/success_v1.txt').read())
success_list = []
success_file_writer = open(
    '/Users/prathyushsp/Development/tf-contrib-analysis/contrib_usage_files/tensorflow.contrib/success_v2.txt', 'a')
error_file_writer = open(
    '/Users/prathyushsp/Development/tf-contrib-analysis/contrib_usage_files/tensorflow.contrib/error.txt', 'a')
# success_file_writer.write(success_list.__str__())

repo_files = glob.glob(
    '/Users/prathyushsp/Development/tf-contrib-analysis/contrib_usage_files/tensorflow.contrib/*.json')

from ratelimit import limits, sleep_and_retry


@sleep_and_retry
@limits(calls=29, period=60)
def call_api(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))
    return response


for fc, repo in enumerate(repos):

    if '/Users/prathyushsp/Development/tf-contrib-analysis/contrib_usage_files/tensorflow.contrib' + repo.replace('/',
                                                                                                                  '_') + '.json' in repo_files:
        print('Skipping: {}'.format(repo))
        continue
    try:
        print('Repository: {} {}/{}'.format(repo, fc, lf))
        # req = requests.get(API_BASE.format(repo)).json()
        req = call_api(API_BASE.format(repo)).json()
        if 'total_count' in req and req['total_count'] == 0:
            continue
        for e, item in enumerate(req['items']):
            content = call_api(item['git_url'] + '?&access_token=').json()
            req['items'][e]['content'] = content
        print('Writing: {}. {} / {} '.format(repo, fc, lf))
        json.dump(req, open(SAVE_DIR + '/{}.json'.format(repo.replace('/', '_')), 'w'))
        success_list.append(repo)
        success_file_writer.write(success_list.__str__())
    except Exception as e:
        print('Encountered Exception: {}'.format(repo))
        import traceback

        json.dump({repo: traceback.format_exc()}, error_file_writer)

success_file_writer.close()
error_file_writer.close()

# for fc, f in enumerate(files):
#     for r_name in json.load(open(f))['items']:
#         print('Repository: {}'.format(r_name['full_name']))
#         req = requests.get(API_BASE.format(r_name['full_name'])).json()
#         time.sleep(2)
#         if 'total_count' in req and req['total_count'] == 0:
#             break
#         for e, item in enumerate(req['items']):
#             content = requests.get(item['git_url']).json()
#             time.sleep(1)
#             req['items'][e]['content'] = content
#         print('Writing {}. {} / {} '.format(r_name['full_name'], fc, lf))
#         json.dump(req, open(SAVE_DIR + '/{}.json'.format(r_name['full_name'].replace('/', '_')), 'w'))


# import os
# print(
#     'https://api.github.com/search/code?q=tf.contrib+repo:{}&per_page=100&access_token=&'.format(
#         'omimo/xRBM'))

#
# content = {
#   "sha": "3a36af69b8378c5eb9dd4546095c01d91b844c89",
#   "node_id": "MDQ6QmxvYjgwOTY3ODgwOjNhMzZhZjY5YjgzNzhjNWViOWRkNDU0NjA5NWMwMWQ5MWI4NDRjODk=",
#   "size": 6250,
#   "url": "https://api.github.com/repos/suriyadeepan/rnn-from-scratch/git/blobs/3a36af69b8378c5eb9dd4546095c01d91b844c89",
#   "content": "aW1wb3J0IHRlbnNvcmZsb3cgYXMgdGYKaW1wb3J0IG51bXB5IGFzIG5wCgpp\nbXBvcnQgZGF0YQppbXBvcnQgdXRpbHMKCmltcG9ydCBhcmdwYXJzZQppbXBv\ncnQgcmFuZG9tCgojIyMjCiMgZGlzYWJsZSBsb2dzCnRmLmxvZ2dpbmcuc2V0\nX3ZlcmJvc2l0eSh0Zi5sb2dnaW5nLkVSUk9SKQojCiMgY2hlY2twb2ludApj\na3B0X3BhdGggPSAnY2twdC92YW5pbGxhMS8nCiMKIyMjCiMgZ2V0IGRhdGEK\nWCwgWSwgaWR4MmNoLCBjaDJpZHggPSBkYXRhLmxvYWRfZGF0YSgnZGF0YS9w\nYXVsZy8nKQojCiMgcGFyYW1zCmhzaXplID0gMjU2Cm51bV9jbGFzc2VzID0g\nbGVuKGlkeDJjaCkKc2VxbGVuID0gWC5zaGFwZVsxXQpzdGF0ZV9zaXplID0g\naHNpemUKQkFUQ0hfU0laRSA9IDEyOAoKCiMgc3RlcCBvcGVyYXRpb24KZGVm\nIHN0ZXAoaHByZXYsIHgpOgogICAgIyBpbml0aWFsaXplcgogICAgeGF2X2lu\naXQgPSB0Zi5jb250cmliLmxheWVycy54YXZpZXJfaW5pdGlhbGl6ZXIKICAg\nICMgcGFyYW1zCiAgICBXID0gdGYuZ2V0X3ZhcmlhYmxlKCdXJywgc2hhcGU9\nW3N0YXRlX3NpemUsIHN0YXRlX3NpemVdLCBpbml0aWFsaXplcj14YXZfaW5p\ndCgpKQogICAgVSA9IHRmLmdldF92YXJpYWJsZSgnVScsIHNoYXBlPVtzdGF0\nZV9zaXplLCBzdGF0ZV9zaXplXSwgaW5pdGlhbGl6ZXI9eGF2X2luaXQoKSkK\nICAgIGIgPSB0Zi5nZXRfdmFyaWFibGUoJ2InLCBzaGFwZT1bc3RhdGVfc2l6\nZV0sIGluaXRpYWxpemVyPXRmLmNvbnN0YW50X2luaXRpYWxpemVyKDAuKSkK\nICAgICMgY3VycmVudCBoaWRkZW4gc3RhdGUKICAgIGggPSB0Zi50YW5oKHRm\nLm1hdG11bChocHJldiwgVykgKyB0Zi5tYXRtdWwoeCxVKSArIGIpCiAgICBy\nZXR1cm4gaAoKIyBwYXJzZSBhcmd1bWVudHMKZGVmIHBhcnNlX2FyZ3MoKToK\nICAgIHBhcnNlciA9IGFyZ3BhcnNlLkFyZ3VtZW50UGFyc2VyKAogICAgICAg\nIGRlc2NyaXB0aW9uPSdWYW5pbGxhIFJlY3VycmVudCBOZXVyYWwgTmV0d29y\nayBmb3IgVGV4dCBIYWxsdWNpbmF0aW9uLCBidWlsdCB3aXRoIHRmLnNjYW4n\nKQogICAgZ3JvdXAgPSBwYXJzZXIuYWRkX211dHVhbGx5X2V4Y2x1c2l2ZV9n\ncm91cChyZXF1aXJlZD1UcnVlKQogICAgZ3JvdXAuYWRkX2FyZ3VtZW50KCct\nZycsICctLWdlbmVyYXRlJywgYWN0aW9uPSdzdG9yZV90cnVlJywKICAgICAg\nICAgICAgICAgICAgICAgICAgaGVscD0nZ2VuZXJhdGUgdGV4dCcpCiAgICBn\ncm91cC5hZGRfYXJndW1lbnQoJy10JywgJy0tdHJhaW4nLCBhY3Rpb249J3N0\nb3JlX3RydWUnLAogICAgICAgICAgICAgICAgICAgICAgICBoZWxwPSd0cmFp\nbiBtb2RlbCcpCiAgICBwYXJzZXIuYWRkX2FyZ3VtZW50KCctbicsICctLW51\nbV93b3JkcycsIHJlcXVpcmVkPUZhbHNlLCB0eXBlPWludCwKICAgICAgICAg\nICAgICAgICAgICAgICAgaGVscD0nbnVtYmVyIG9mIHdvcmRzIHRvIGdlbmVy\nYXRlJykKICAgIGFyZ3MgPSB2YXJzKHBhcnNlci5wYXJzZV9hcmdzKCkpCiAg\nICByZXR1cm4gYXJncwoKIAppZiBfX25hbWVfXyA9PSAnX19tYWluX18nOgog\nICAgIwogICAgIyBwYXJzZSBhcmd1bWVudHMKICAgIGFyZ3MgPSBwYXJzZV9h\ncmdzKCkKICAgICMKICAgICMgYnVpbGQgZ3JhcGgKICAgIHRmLnJlc2V0X2Rl\nZmF1bHRfZ3JhcGgoKQogICAgIyBpbnB1dHMKICAgIHhzXyA9IHRmLnBsYWNl\naG9sZGVyKHNoYXBlPVtOb25lLCBOb25lXSwgZHR5cGU9dGYuaW50MzIpCiAg\nICB5c18gPSB0Zi5wbGFjZWhvbGRlcihzaGFwZT1bTm9uZV0sIGR0eXBlPXRm\nLmludDMyKQogICAgIwogICAgIyBlbWJlZGRpbmdzCiAgICBlbWJzID0gdGYu\nZ2V0X3ZhcmlhYmxlKCdlbWInLCBbbnVtX2NsYXNzZXMsIHN0YXRlX3NpemVd\nKQogICAgcm5uX2lucHV0cyA9IHRmLm5uLmVtYmVkZGluZ19sb29rdXAoZW1i\ncywgeHNfKQogICAgIwogICAgIyBpbml0aWFsIGhpZGRlbiBzdGF0ZQogICAg\naW5pdF9zdGF0ZSA9IHRmLnBsYWNlaG9sZGVyKHNoYXBlPVtOb25lLCBzdGF0\nZV9zaXplXSwgZHR5cGU9dGYuZmxvYXQzMiwgbmFtZT0naW5pdGlhbF9zdGF0\nZScpCiAgICAjCiAgICAjIGhlcmUgY29tZXMgdGhlIHNjYW4gb3BlcmF0aW9u\nOyB3YWtlIHVwIQogICAgIyAgIHRmLnNjYW4oZm4sIGVsZW1zLCBpbml0aWFs\naXplcikKICAgIHN0YXRlcyA9IHRmLnNjYW4oc3RlcCwgCiAgICAgICAgICAg\nIHRmLnRyYW5zcG9zZShybm5faW5wdXRzLCBbMSwwLDJdKSwKICAgICAgICAg\nICAgaW5pdGlhbGl6ZXI9aW5pdF9zdGF0ZSkgCiAgICAjIyMKICAgICMgc2V0\nIGxhc3Qgc3RhdGUKICAgIGxhc3Rfc3RhdGUgPSBzdGF0ZXNbLTFdCiAgICBz\ndGF0ZXMgPSB0Zi50cmFuc3Bvc2Uoc3RhdGVzLCBbMSwwLDJdKQogICAgIwog\nICAgIyBwcmVkaWN0aW9ucwogICAgViA9IHRmLmdldF92YXJpYWJsZSgnVics\nIHNoYXBlPVtzdGF0ZV9zaXplLCBudW1fY2xhc3Nlc10sIAogICAgICAgICAg\nICAgICAgICAgICAgICBpbml0aWFsaXplcj10Zi5jb250cmliLmxheWVycy54\nYXZpZXJfaW5pdGlhbGl6ZXIoKSkKICAgIGJvID0gdGYuZ2V0X3ZhcmlhYmxl\nKCdibycsIHNoYXBlPVtudW1fY2xhc3Nlc10sIAogICAgICAgICAgICAgICAg\nICAgICAgICAgaW5pdGlhbGl6ZXI9dGYuY29uc3RhbnRfaW5pdGlhbGl6ZXIo\nMC4pKQogICAgIwogICAgIyBmbGF0dGVuIHN0YXRlcyB0byAyZCBtYXRyaXgg\nZm9yIG1hdG11bHQgd2l0aCBWCiAgICBzdGF0ZXNfcmVzaGFwZWQgPSB0Zi5y\nZXNoYXBlKHN0YXRlcywgWy0xLCBzdGF0ZV9zaXplXSkKICAgIGxvZ2l0cyA9\nIHRmLm1hdG11bChzdGF0ZXNfcmVzaGFwZWQsIFYpICsgYm8KICAgIHByZWRp\nY3Rpb25zID0gdGYubm4uc29mdG1heChsb2dpdHMpCiAgICAjCiAgICAjIG9w\ndGltaXphdGlvbgogICAgbG9zc2VzID0gdGYubm4uc3BhcnNlX3NvZnRtYXhf\nY3Jvc3NfZW50cm9weV93aXRoX2xvZ2l0cyhsb2dpdHMsIHlzXykKICAgIGxv\nc3MgPSB0Zi5yZWR1Y2VfbWVhbihsb3NzZXMpCiAgICB0cmFpbl9vcCA9IHRm\nLnRyYWluLkFkYW1PcHRpbWl6ZXIobGVhcm5pbmdfcmF0ZT0wLjEpLm1pbmlt\naXplKGxvc3MpCiAgICAjIAogICAgIyB0byBnZW5lcmF0ZSBvciB0byB0cmFp\nbiAtIHRoYXQgaXMgdGhlIHF1ZXN0aW9uLgogICAgaWYgYXJnc1sndHJhaW4n\nXToKICAgICAgICAjIAogICAgICAgICMgdHJhaW5pbmcKICAgICAgICAjICBz\nZXR1cCBiYXRjaGVzIGZvciB0cmFpbmluZwogICAgICAgIGVwb2NocyA9IDUw\nCiAgICAgICAgIwogICAgICAgICMgc2V0IGJhdGNoIHNpemUKICAgICAgICBi\nYXRjaF9zaXplID0gQkFUQ0hfU0laRQogICAgICAgIHRyYWluX3NldCA9IHV0\naWxzLnJhbmRfYmF0Y2hfZ2VuKFgsWSxiYXRjaF9zaXplPWJhdGNoX3NpemUp\nCiAgICAgICAgIyB0cmFpbmluZyBzZXNzaW9uCiAgICAgICAgd2l0aCB0Zi5T\nZXNzaW9uKCkgYXMgc2VzczoKICAgICAgICAgICAgc2Vzcy5ydW4odGYuZ2xv\nYmFsX3ZhcmlhYmxlc19pbml0aWFsaXplcigpKQogICAgICAgICAgICB0cmFp\nbl9sb3NzID0gMAogICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICBm\nb3IgaSBpbiByYW5nZShlcG9jaHMpOgogICAgICAgICAgICAgICAgICAgIGZv\nciBqIGluIHJhbmdlKDEwMDApOgogICAgICAgICAgICAgICAgICAgICAgICB4\ncywgeXMgPSB0cmFpbl9zZXQuX19uZXh0X18oKQogICAgICAgICAgICAgICAg\nICAgICAgICBfLCB0cmFpbl9sb3NzXyA9IHNlc3MucnVuKFt0cmFpbl9vcCwg\nbG9zc10sIGZlZWRfZGljdCA9IHsKICAgICAgICAgICAgICAgICAgICAgICAg\nICAgICAgICB4c18gOiB4cywKICAgICAgICAgICAgICAgICAgICAgICAgICAg\nICAgICB5c18gOiB5cy5yZXNoYXBlKFtiYXRjaF9zaXplKnNlcWxlbl0pLAog\nICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGluaXRfc3RhdGUgOiBu\ncC56ZXJvcyhbYmF0Y2hfc2l6ZSwgc3RhdGVfc2l6ZV0pCiAgICAgICAgICAg\nICAgICAgICAgICAgICAgICB9KQogICAgICAgICAgICAgICAgICAgICAgICB0\ncmFpbl9sb3NzICs9IHRyYWluX2xvc3NfCiAgICAgICAgICAgICAgICAgICAg\ncHJpbnQoJ1t7fV0gbG9zcyA6IHt9Jy5mb3JtYXQoaSx0cmFpbl9sb3NzLzEw\nMDApKQogICAgICAgICAgICAgICAgICAgIHRyYWluX2xvc3MgPSAwCiAgICAg\nICAgICAgIGV4Y2VwdCBLZXlib2FyZEludGVycnVwdDoKICAgICAgICAgICAg\nICAgIHByaW50KCdpbnRlcnJ1cHRlZCBieSB1c2VyIGF0ICcgKyBzdHIoaSkp\nCiAgICAgICAgICAgICAgICAjCiAgICAgICAgICAgICAgICAjIHRyYWluaW5n\nIGVuZHMgaGVyZTsgCiAgICAgICAgICAgICAgICAjICBzYXZlIGNoZWNrcG9p\nbnQKICAgICAgICAgICAgICAgIHNhdmVyID0gdGYudHJhaW4uU2F2ZXIoKQog\nICAgICAgICAgICAgICAgc2F2ZXIuc2F2ZShzZXNzLCBja3B0X3BhdGggKyAn\ndmFuaWxsYTEuY2twdCcsIGdsb2JhbF9zdGVwPWkpCiAgICBlbGlmIGFyZ3Nb\nJ2dlbmVyYXRlJ106CiAgICAgICAgIwogICAgICAgICMgZ2VuZXJhdGUgdGV4\ndAogICAgICAgIHJhbmRvbV9pbml0X3dvcmQgPSByYW5kb20uY2hvaWNlKGlk\neDJjaCkKICAgICAgICBjdXJyZW50X3dvcmQgPSBjaDJpZHhbcmFuZG9tX2lu\naXRfd29yZF0KICAgICAgICAjCiAgICAgICAgIyBzdGFydCBzZXNzaW9uCiAg\nICAgICAgd2l0aCB0Zi5TZXNzaW9uKCkgYXMgc2VzczoKICAgICAgICAgICAg\nIyBpbml0IHNlc3Npb24KICAgICAgICAgICAgc2Vzcy5ydW4odGYuZ2xvYmFs\nX3ZhcmlhYmxlc19pbml0aWFsaXplcigpKQogICAgICAgICAgICAjCiAgICAg\nICAgICAgICMgcmVzdG9yZSBzZXNzaW9uCiAgICAgICAgICAgIGNrcHQgPSB0\nZi50cmFpbi5nZXRfY2hlY2twb2ludF9zdGF0ZShja3B0X3BhdGgpCiAgICAg\nICAgICAgIHNhdmVyID0gdGYudHJhaW4uU2F2ZXIoKQogICAgICAgICAgICBp\nZiBja3B0IGFuZCBja3B0Lm1vZGVsX2NoZWNrcG9pbnRfcGF0aDoKICAgICAg\nICAgICAgICAgIHNhdmVyLnJlc3RvcmUoc2VzcywgY2twdC5tb2RlbF9jaGVj\na3BvaW50X3BhdGgpCiAgICAgICAgICAgICMgZ2VuZXJhdGUgb3BlcmF0aW9u\nCiAgICAgICAgICAgIHdvcmRzID0gW2N1cnJlbnRfd29yZF0KICAgICAgICAg\nICAgc3RhdGUgPSBOb25lCiAgICAgICAgICAgICMgc2V0IGJhdGNoX3NpemUg\ndG8gMQogICAgICAgICAgICBiYXRjaF9zaXplID0gMQogICAgICAgICAgICBu\ndW1fd29yZHMgPSBhcmdzWydudW1fd29yZHMnXSBpZiBhcmdzWydudW1fd29y\nZHMnXSBlbHNlIDExMQogICAgICAgICAgICAjIGVudGVyIHRoZSBsb29wCiAg\nICAgICAgICAgIGZvciBpIGluIHJhbmdlKG51bV93b3Jkcyk6CiAgICAgICAg\nICAgICAgICBpZiBzdGF0ZToKICAgICAgICAgICAgICAgICAgICBmZWVkX2Rp\nY3QgPSB7IHhzXyA6IG5wLmFycmF5KGN1cnJlbnRfd29yZCkucmVzaGFwZShb\nMSwgMV0pLCAKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGluaXRfc3Rh\ndGUgOiBzdGF0ZV8gfQogICAgICAgICAgICAgICAgZWxzZToKICAgICAgICAg\nICAgICAgICAgICBmZWVkX2RpY3QgPSB7IHhzXyA6IG5wLmFycmF5KGN1cnJl\nbnRfd29yZCkucmVzaGFwZShbMSwxXSkKICAgICAgICAgICAgICAgICAgICAg\nICAgICAgICwgaW5pdF9zdGF0ZSA6IG5wLnplcm9zKFtiYXRjaF9zaXplLCBz\ndGF0ZV9zaXplXSkgfQogICAgICAgICAgICAgICAgIwogICAgICAgICAgICAg\nICAgIyBmb3J3YXJkIHByb3BhZ2F0aW9uCiAgICAgICAgICAgICAgICBwcmVk\ncywgc3RhdGVfID0gc2Vzcy5ydW4oW3ByZWRpY3Rpb25zLCBsYXN0X3N0YXRl\nXSwgZmVlZF9kaWN0PWZlZWRfZGljdCkKICAgICAgICAgICAgICAgICMgCiAg\nICAgICAgICAgICAgICAjIHNldCBmbGFnIHRvIHRydWUKICAgICAgICAgICAg\nICAgIHN0YXRlID0gVHJ1ZQogICAgICAgICAgICAgICAgIyAKICAgICAgICAg\nICAgICAgICMgc2V0IG5ldyB3b3JkCiAgICAgICAgICAgICAgICBjdXJyZW50\nX3dvcmQgPSBucC5yYW5kb20uY2hvaWNlKHByZWRzLnNoYXBlWy0xXSwgMSwg\ncD1ucC5zcXVlZXplKHByZWRzKSlbMF0KICAgICAgICAgICAgICAgICMgYWRk\nIHRvIGxpc3Qgb2Ygd29yZHMKICAgICAgICAgICAgICAgIHdvcmRzLmFwcGVu\nZChjdXJyZW50X3dvcmQpCiAgICAgICAgIyMjIyMjIyMjCiAgICAgICAgIyB0\nZXh0IGdlbmVyYXRpb24gY29tcGxldGUKICAgICAgICAjCiAgICAgICAgcHJp\nbnQoJ19fX19fX0dlbmVyYXRlZCBUZXh0X19fX19fXycpCiAgICAgICAgcHJp\nbnQoJycuam9pbihbaWR4MmNoW3ddIGZvciB3IGluIHdvcmRzXSkpCiAgICAg\nICAgcHJpbnQoJ19fX19fX19fX19fX19fX19fX19fX19fX19fXycpCg==\n",
#   "encoding": "base64"
# }
#
# import  base64
# print(base64.b64decode(content['content']))
