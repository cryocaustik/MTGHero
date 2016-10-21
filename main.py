import time
from tokens import GetTokens
from slackclient import SlackClient
from card_search import CardFinder


token = GetTokens().slack_bot()
client = SlackClient(token)
card_name = None


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

                    with CardFinder(parsed[1:], 'online') as cf:
                        card_name = cf

                    if len(card_name) > 0:
                        multiverse_id = card_name['multiverseid']
                        url_prefix = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%s&amp;type=card'
                        message_string = url_prefix % multiverse_id
                        client.rtm_send_message(message_channel, '%s' % (message_string))
                    else:
                        client.rtm_send_message(message_channel, 'sorry, no match found!')

                    print('found: ', card_name)

                ## ~/ clean up
                parsed = None
                card_name = None
            except:
                pass
        time.sleep(1)
