# -*- coding: utf-8 -*-
from utilies import *
import random

commands = [
    '^image',
    '^img',
    '^i ',
    '^insfw'
]

parameters = {('query', True)}

description = 'This command performs a Google Images search for the given query. One random top result is returned. Safe search is enabled by default; use *' + config['command_start'] + 'insfw* to get potentially NSFW results.'
action = 'upload_photo'

exts = {
    '.jpg$',
    '.jpeg$',
    '.gif$',
    '.png$',
    '.tif$',
    '.bmp$'
}


def run(msg):
    input = get_input(msg['text'])

    if not input:
        doc = get_doc(commands, parameters, description)
        return send_message(msg['chat']['id'], doc, parse_mode="Markdown")

    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'searchType': 'image',
        'safe': 'medium',
        'key': config['api']['googledev'],
        'cx': '011243947282844107040:nwg-q67c7wa',
        'q': input
    }

    if get_command(msg['text']) == 'insfw':
        params['safe'] = 'off'

    jstr = requests.get(url, params=params)

    if jstr.status_code != 200:
        return send_error(msg, 'connection')

    jdat = json.loads(jstr.text)

    if jdat['searchInformation']['totalResults'] == '0':
        return send_error(msg, 'results')

    is_real = False
    counter = 0
    while not is_real:
        counter = counter + 1
        if counter > 5 or jdat['searchInformation']['totalResults'] == '0':
            return send_error(msg, 'results')

        i = random.randint(1, len(jdat['items']))-1

        result_url = jdat['items'][i]['link']
        #caption = jdat['items'][i]['snippet']
        caption = '"' + input + '"'

        for v in exts:
            if re.compile(v).search(result_url):
                is_real = True

    photo = download(result_url)

    if photo:
        send_photo(msg['chat']['id'], photo, caption=caption)
    else:
        send_error(msg, 'download')
