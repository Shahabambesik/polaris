# -*- coding: utf-8 -*-
from utils import *
import random

commands = [
    '^define',
    '^ud',
    '^urbandictionary'
]

parameters = {('term', True)}
description = 'Returns the first definition for a given term from [Urban Dictionary](http://urbandictionary.com).'
action = 'typing'


def run(msg):
    input = get_input(msg['text'])

    if not input:
        doc = get_doc(commands, parameters, description)
        return send_message(msg['chat']['id'], doc, parse_mode="Markdown")

    url = 'http://api.urbandictionary.com/v0/define'
    params = {'term': input}

    jdat = send_request(url, params)

    if not jdat:
        return send_error(msg, 'connection')

    if jdat['result_type'] == 'no_results':
        return send_error(msg, 'results')

    i = random.randint(1, len(jdat['list'])) - 1

    text = '*' + jdat['list'][i]['word'] + '*\n'
    text += jdat['list'][i]['definition'] + '\n'
    if jdat['list'][i]['example']:
        text += '\nExample:\n_' + jdat['list'][i]['example'] + '_'

    send_message(msg['chat']['id'], text, parse_mode="Markdown")

def inline(qry):
    input = get_input(qry['query'])

    url = 'http://api.urbandictionary.com/v0/define'
    params = {'term': input}

    jdat = send_request(url, params)

    results_json = []
    for item in jdat['list']:
        text = '*' + item['word'] + '*\n'
        if len(item['definition']) > 400:
            text += item['definition'][:400] + '...\n'
        else:
            text += item['definition'] + '\n'
        if item['example'] and len(item['example']) < 80:
            text += '\nExample:\n_' + item['example'] + '_'
        text += '\n' + item['permalink'][:400]

        result = {
            'type': 'article',
            'id': str(item['defid']),
            'title': item['word'] + ' (' + item['author'] + ')',
            'message_text': text,
            'description': item['definition'],
            'url': item['permalink'],
            'thumb_url': 'http://fa2png.io/media/icons/fa-quote-left/96/16/673ab7_ffffff.png',
            'thumb_width': 128,
            'thumb_height': 128,
            'parse_mode': 'Markdown',
            'disable_web_page_preview': True
        }
        if len(text) <= 512:
            results_json.append(result)

    results = json.dumps(results_json)
    answer_inline_query(qry['id'], results)
