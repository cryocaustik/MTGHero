import json
from urllib.request import  urlopen


class CardFinder:
    db_path = None
    db_url = None
    db_source = None
    card_name = None
    results = None

    def __init__(self, cardname, source):
        CardFinder.db_path = r'/home/user/AllSets.json'
        CardFinder.db_url = r'https://mtgjson.com/json/AllSets.json'
        CardFinder.card_name = str(cardname)
        CardFinder.results = {}

        if source in ['local', 'online']:
            CardFinder.db_source = source
        else:
            CardFinder.db_source = 'online'

    def __enter__(self):
        if CardFinder.db_source == 'local':
            return CardFinder.find_card_local(self)
        elif CardFinder.db_source == 'online':
            return CardFinder.find_card_online(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        CardFinder.db_path = None
        CardFinder.db_url = None
        CardFinder.card_name = None
        CardFinder.results = None
        print('exiting')

    def find_card_local(self):
        name = CardFinder.card_name
        with open(CardFinder.db_path, 'r') as f:
            card_db = json.load(f)
            f.close()

        for card_set in card_db:
            for card_name in card_db[card_set]["cards"]:
                if str(card_name["name"]).upper() == name.upper():
                    for key in card_name:
                        CardFinder.results[key] = card_name[key]

        return CardFinder.results

    def find_card_online(self):
        name = CardFinder.card_name
        json_url = urlopen(CardFinder.db_url).read()
        card_db = json.loads(json_url.decode('utf-8'))

        for card_set in card_db:
            for card_name in card_db[card_set]["cards"]:
                if str(card_name["name"]).upper() == name.upper():
                    for key in card_name:
                        CardFinder.results[key] = card_name[key]

        return CardFinder.results

## for debugging
# c_name = 'angel of invention'
# with CardFinder(c_name, 'online') as cf:
#     print(cf)

