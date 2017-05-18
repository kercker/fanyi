import json
import os
import pickle
import random
import time
import sys

from hashlib import md5
from os import path

import requests

from tk_generator import get_tk

CURDIR = path.dirname(path.abspath(__file__))
UA = (
        'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:53.0)'
        ' Gecko/20100101 Firefox/53.0'
        )

def baidu(word):
    url = 'https://fanyi.baidu.com/v2transapi'
    headers = { 
        'User-Agent': UA,
        'Referer': 'https://fanyi.baidu.com/'}
    data = {
            'from':'en',
            'to': 'zh',
            'query': word,
            'simple_means_flag': '3'
            } 
    res = requests.post(url, data=data, headers=headers)
    res = json.loads(res.content)
    return res['trans_result']['data'][0]['dst']

def bing(word):
    url = (
            'https://www.bing.com/translator/'
            'api/Translate/TranslateArray?from=-&to=zh-CHS'
            )
    bingsess = path.join(CURDIR, 'bing.pkl')
    if os.access(bingsess, os.F_OK):
        with open(bingsess) as f:
            sess = pickle.load(f)
        res = sess.post(url, json=[{'text':word}])
        if res.status_code == 200:
            res = json.loads(res.content)
            return res['items'][0]['text']
    sess = requests.Session()
    headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json; charset=utf-8',
            'Host': 'www.bing.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.bing.com/translator',
            'User-Agent': UA,
            'X-Requested-With': 'XMLHttpRequest'}
    res = sess.get('https://www.bing.com/translator', headers=headers)
    with open(bingsess, 'w') as f:
        pickle.dump(sess, f)
    res = sess.post(url, json=[{'text':word}])
    res = json.loads(res.content)
    return res['items'][0]['text']

def ydenc(word):
    u = 'fanyideskweb'
    f = '%s%s' % (int(time.time()*1000), random.randint(0, 9))
    d = word
    c = "rY0D^0'nM0}g5Mm1z%1G4"
    hexdigest = md5(u+d+f+c).hexdigest()
    return (f, hexdigest)

def youdao(word):
    url = (
            'http://fanyi.youdao.com/translate_o'
            '?smartresult=dict&smartresult=rule&sessionFrom=null'
            )
    f, g = ydenc(word)
    data = {
            'i': word,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': str(f),
            'sign': g,
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTON',
            'typoResult': 'true'}
    headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'fanyi.youdao.com',
            'Referer': 'http://fanyi.youdao.com/',
            'User-Agent': UA,
            'X-Requested-With': 'XMLHttpRequest'}
    res = requests.post(url, data=data, headers=headers)
    res = json.loads(res.content)
    return res['translateResult'][0][0]['tgt']

def google(word):
    tk = get_tk(word)
    url = (
            'https://translate.google.com/translate_a/single?'
            'client=t&sl=auto&tl=zh-CN&hl=en&dt=at&dt=bd&dt=ex'
            '&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8'
            '&oe=UTF-8&source=btn&ssel=0&tsel=4&kc=0&tk=%s&q=%s'
            ) % (tk, word)
    headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'translate.google.com',
            'Referer': 'https://translate.google.com/',
            'User-Agent': UA}
    res = requests.get(url, headers=headers)
    res = json.loads(res.content)
    return res[0][0][0]

def fanyi(word):
    print 'baidu:', baidu(word)
    print 'youdao:', youdao(word)
    print 'bing:', bing(word)
    print 'google', google(word)

if __name__ == '__main__':
    fanyi(sys.argv[1])