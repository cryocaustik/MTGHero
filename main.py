import os
import time
from slackclient import SlackClient
from card_search import CardFinder

os.environ["SLACK_BOT_TOKEN"] = r''

client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
card_name = ''


if client.rtm_connect():
    while True:
        last_read = client.rtm_read()

        if last_read:
            try:
                parsed = last_read[0]['text']
                message_channel = last_read[0]['channel']

                if parsed and parsed[0] == '!':
                    print(parsed)
                    client.rtm_send_message(message_channel, 'searching...')

                    cf = CardFinder()
                    card_name = cf.find_card_online(parsed[1:])
                    time.sleep(5)

                    if len(card_name) > 0:
                        multiverse_id = card_name['multiverseid']
                        url_prefix = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%s&amp;type=card'
                        message_string = url_prefix % multiverse_id
                        client.rtm_send_message(message_channel, '%s' % (message_string))

                        # client.rtm_send_message(message_channel, str(card_name))
                        # for key in card_name:
                        #     client.rtm_send_message(message_channel, '%s: %s' % (str(key), card_name[key]))
                    else:
                        client.rtm_send_message(message_channel, 'sorry, no match found!')

                    print('found: ', card_name)

                    #clean up
                    card_name = None
                    parsed = None
                    cf = None
                    multiverse_id = None
                    message_string = None
            except:
                pass
        time.sleep(1)
