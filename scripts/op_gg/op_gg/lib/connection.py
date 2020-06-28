import json
from collections import deque

from redis import Redis


class Connection:
    def __init__(self, *args, **kwargs):
        self.connector = Redis(*args, **kwargs)
        self.queue = deque()

        try:
            for item in json.loads(self.connector.get('crawl-queue')):
                self.queue.append(item)
        except:
            self.queue.append('Maydev')

    def commit(self):
        self.connector.set('crawl-queue', json.dumps(list(self.queue)))

    def get_champion(self, champion: str):
        prefix = 'champion'
        return type('Champion', (object,), json.loads(
            self.connector.get(f'{prefix}:{champion}')))

    def get_summoner(self, summoner: str):
        prefix = 'summoner'
        return type('Summoner', (object,), json.loads(
            self.connector.get(f'{prefix}:{summoner}')))

    def get_summoner_champion(self, summoner: str, champion: str):
        prefix = 'summoner-champion-'
        return type('SummonerChampion', (object,), json.loads(
            self.connector.get(f'{prefix}{summoner}:{champion}')))

    def set_champion(self, champion: str, data: object):
        prefix = 'champion'
        self.connector.set(f'{prefix}:{champion}', json.dumps(data))
    
    def set_champions(self, champions: dict):
        prefix = 'champion'
        self.connector.mset(
            {f'{prefix}:{key}': value for key, value in champions})

    def set_summoner(self, summoner: str, data: object):
        prefix = 'summoner'
        self.connector.set(f'{prefix}:{summoner}', json.dumps(data))

    def set_summoners(self, summoners: dict):
        prefix = 'summoner'
        self.connector.mset(
            {f'{prefix}:{key}': value for key, value in summoners})

    def set_summoner_champion(self, summoner:str, champion: str, data: object):
        prefix = 'summoner-champion-'
        self.connector.set(f'{prefix}{summoner}:{champion}', json.dumps(data))

    def set_summoner_champions(self, summoner:str, champions: dict):
        prefix = 'summoner-champion-'
        self.connector.mset(
            {f'{prefix}{summoner}:{key}': value for key, value in champions})

    @property
    def champions(self):
        prefix = 'champion'
        for champion in self.connector.scan_iter(f'{prefix}:*'):
            yield champion[len(prefix) + 1:]

    @property
    def summoners(self):
        prefix = 'summoner'
        for summoner in self.connector.scan_iter(f'{prefix}:*'):
            yield summoner[len(prefix) + 1:]

    @property
    def summoner_champions(self, summoner: str):
        prefix = 'summoner-champion-'
        for champion in self.connector.scan_iter(f'{prefix}{summoner}:*'):
            yield champion[len(prefix) + 1:]
