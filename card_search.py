import time
import json
from urllib.request import  urlopen


class CardFinder:
    db_path = r'/home/user/AllSets.json'
    db_url = r'https://mtgjson.com/json/AllSets.json'
    db_source = None
    card_name = None
    results = {}

    def __init__(self):
        CardFinder.db_source = 'local'

    # def __enter__(self):
    #     CardFinder.db_path = r'/home/cryo/Google Drive/Scripts and Solutions/Python/MTGhero_bot/AllSets.json'
    #     CardFinder.db_url = r'https://mtgjson.com/json/AllSets.json'
    #     CardFinder.db_source = None
    #     CardFinder.card_name = None
    #     CardFinder.results = {}
    #     # return self.find_card_local()
    #
    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     CardFinder.card_name = None
    #     CardFinder.db_source = None
    #     CardFinder.results = None
    #     CardFinder.db_path = None
    #     CardFinder.db_path = None

    def find_card_local(self, name):

        with open(CardFinder.db_path, 'r') as f:
            card_db = json.load(f)
            f.close()

        for card_set in card_db:
            for card_name in card_db[card_set]["cards"]:
                if str(card_name["name"]).upper() == name.upper():
                    for key in card_name:
                        CardFinder.results[key] = card_name[key]

        return CardFinder.results

    def find_card_online(self, name):

        json_url = urlopen(CardFinder.db_url).read()
        card_db = json.loads(json_url.decode('utf-8'))

        for card_set in card_db:
            for card_name in card_db[card_set]["cards"]:
                if str(card_name["name"]).upper() == name.upper():
                    for key in card_name:
                        CardFinder.results[key] = card_name[key]

        return CardFinder.results

# cf = CardFinder()
# print(cf.find_card_local('angel of invention'))
