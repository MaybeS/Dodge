from functools import partial

from core.lib.cached_property import cached_property
from core.models import Serialize
from .champion import Champion


class Summoner(Serialize):
    def __init__(self, name: str, lazy: bool = True):
        super().__init__('mmr', 'wins', 'losses', 'champions')
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Name: {self.name}'

    @cached_property
    def context_summoner(self):
        return bs(requests.get(url_summoner.format(name=self.name)).text, 'html.parser')

    @cached_property
    def context_champions(self):
        return bs(requests.get(url_champions.format(name=self.name)).text, 'html.parser')

    @cached_property
    def info(self):
        def rank_to_mmr(rank):
            ranks = ['Iron', 'Bronze', 'Silver', 'Gold', 'Platinum',
                     'Diamond', 'Master', 'GrandMaster', 'Challenger']
            rank_name, *rank_index = rank.split(' ')
            rank_index, *_ = rank_index or (0,)

            # Ignore GrandMaster and Challenger index
            return (min(ranks.index(rank_name), 6) + 1) * 400 - int(rank_index) * 100

        rank = self.context_summoner.find(
            'div', {'class': 'TierRank'}).text.strip()

        # Ignore Unranked
        if rank == 'Unranked':
            return 0, 0, 0

        rank_points, *_ = self.context_summoner.find(
            'span', {'class': 'LeaguePoints'}).text.split(' ')
        wins = int(self.context_summoner.find(
            'span', {'class': 'wins'}).text[:-1])
        losses = int(self.context_summoner.find(
            'span', {'class': 'losses'}).text[:-1])
        mmr = rank_to_mmr(rank) + int(rank_points)

        return mmr, wins, losses

    @cached_property
    def mmr(self):
        return self.info[0]

    @cached_property
    def wins(self):
        return self.info[1]

    @cached_property
    def losses(self):
        return self.info[2]

    @cached_property
    def champions(self):
        return tuple(map(partial(Champion, self), self.context_champions.findAll('tr', {'class', 'Row'})[1:]))

    @property
    def played_with(self):
        for div in self.context_summoner.findAll('div', {'class': 'SummonerName'}):
            yield Summoner(div.text.strip())
