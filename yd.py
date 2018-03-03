import sys
import requests
import random
import argparse
from bs4 import BeautifulSoup
from collections import defaultdict
from hashlib import md5


def ydapi(q, fromLang='zh-CHS', toLang='EN'):
    """
    youdao translation api interface
    q: string type encoding utf-8
    language: ['zh-CHS', 'EN', 'ja', 'ko', 'fr', 'ru', 'pt', 'es']
    """
    appKey = '**************'
    secretKey = '********************'
    url = 'http://openapi.youdao.com/api'
    salt = random.randint(1, 65536)
    sign = appKey+q+str(salt)+secretKey
    m = md5(sign.encode('utf-8')) 
    sign = m.hexdigest()
    params = {'q':q, 'from':fromLang, 'to':toLang,\
         'appKey': appKey, 'salt': str(salt), 'sign': sign}
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        dic = r.json()
    except:
        return None
    return dic


def ydword(word):
    url = "http://dict.youdao.com/search"
    header = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
    headers = {'user-agent': header}
    word = {'q':word}
    try:
        r = requests.get(url=url, params=word, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def ydparser(html):
    translate_dict = defaultdict(list)
    soup = BeautifulSoup(html, 'html.parser')
    try:
        keyword = soup.find('span', class_='keyword').get_text()
        trans = soup.find('div', class_='trans-container')
        if ord(keyword[0]) > 127:
            direction = True
        else:
            direction = False
    except:
        return None
    if direction:
        for group in trans.find_all('p', class_='wordGroup'):
            pos = group.find('span').get_text().strip()
            if not '.' in pos:
                pos = '.'
            english = []
            for wd in group.find_all('a'):
                english.append(wd.get_text())
            translate_dict[pos] = english
    else:
        for group in trans.find_all('li'):
            text_str = group.get_text()
            if not '.' in text_str:
                pos = '.'
                chinese = text_str
            else:
                text_str = text_str.split('.')
                pos = text_str[0]
                chinese = text_str[-1]
            translate_dict[pos].append(chinese)
    return translate_dict


def ydprint(res_dict, out_file='stdout'):
    if type(res_dict) == type({}):
        if res_dict['errorCode'] == '0':
            print(res_dict['query'])
            print('-'*80)
            trans_str = ''.join(res_dict['translation'])
            print(trans_str)
            if out_file != 'stdout':
                with open(out_file, 'w') as fw:
                    fw.write(trans_str)
        else:
            print('API.errorCode:', ''.join(res_dict['errorCode']))
    else:
        for key in res_dict:
            value = res_dict[key]
            if key != '.':
                format_str = key + '\t' + ', '.join(value)
            else:
                format_str = ', '.join(value)
            print(format_str)


def main():
    parser = argparse.ArgumentParser(description="Youdao Translation CLI. Author: claylau")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-w", dest="word", type=str, \
                        help="the word to translate using yd-dict web interface.")
    group.add_argument("-t", dest="text", type=str, \
                        help="the text to translate using yd-fanyi api.")
    group.add_argument("-f", dest="file", type=str, \
                        help="the file path of text to translate using yd-fanyi api.")
    parser.add_argument("-o", dest="output", type=str, \
                        help="to save the translatin file when -f effects.")
    args = parser.parse_args()
    if args.word:
        word = args.word
        html = ydword(word)
        if html != "":
            result = ydparser(html)
            if result:
                ydprint(result)
            else:
                print("Word translate error.")
        else:
            print("Web request falied.")
    if args.text:
        text = args.text
        if ord(text[0]) <= 127:
            fromLang = 'EN'
            toLang = 'zh-CHS'
            dic = ydapi(text, fromLang, toLang)
        else:
            dic = ydapi(text)
        if args.output:
            out_file = args.output
        else:
            out_file = 'stdout'
        ydprint(dic, out_file)
    if args.file:
        file = args.file
        with open(file, 'r') as fr:
            txt = fr.read()
            if len(txt) >= 5000:
                txt = txt[:5000]
            if ord(txt[0]) <= 127:
                fromLang = 'EN'
                toLang = 'zh-CHS'
                dic = ydapi(txt, fromLang, toLang)
            else:
                dic = ydapi(txt)
        if args.output:
            out_file = args.output
        else:
            out_file = 'stdout'
        ydprint(dic, out_file)


if __name__ == '__main__':
    main()
