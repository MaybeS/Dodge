from core.lib.cached_property import cached_property
from core.models import Serialize
from .summoner import Summoner


class Champion(Serialize):
    def __init__(self, summoner: Summoner, context):
        super().__init__('name', 'wins', 'losses', 'KDA', 'gold', 'cs', 'max_kill', 'max_death', 'ADD', 'ADT', 
                         'double_kill', 'triple_kill', 'quadra_kill', 'penta_kill');
        self.summoner = summoner
        self.context = context
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f'{self.name} ({self.summoner})'
    
    @cached_property
    def name(self):
        return self.context.find('td', {'class', 'ChampionName'}).text.strip()
    @cached_property
    def wins(self):
        return int(self.extract(self.context.find('div', {'class': 'Text Left'}), '0W')[:-1])
    @cached_property
    def losses(self):
        return int(self.extract(self.context.find('div', {'class': 'Text Right'}), '0L')[:-1])
    @cached_property
    def KDA(self):
        return tuple(map(float, self.context.find('div', {'class': 'KDA'}).text.replace('/', '').split()))
    @cached_property
    def extras(self):
        return tuple(map(lambda v: self.refine(v.replace(',', ''), 0), 
                         map(str.strip, (
                             map(self.extract, self.context.findAll('td', {'class', 'Value Cell'}))))))
    @cached_property
    def gold(self):
        return self.extras[0]
    @cached_property
    def cs(self):
        return self.extras[1]
    @cached_property
    def max_kill(self):
        return self.extras[2]
    @cached_property
    def max_death(self):
        return self.extras[3]
    @cached_property
    def ADD(self):
        return self.extras[4]
    @cached_property
    def ADT(self):
        return self.extras[5]
    @cached_property
    def double_kill(self):
        return self.extras[6]
    @cached_property
    def triple_kill(self):
        return self.extras[7]
    @cached_property
    def quadra_kill(self):
        return self.extras[8]
    @cached_property
    def penta_kill(self):
        return self.extras[9]
    
    @staticmethod
    def extract(node, default=''):
        try:
            return node.text
        except AttributeError:
            return default

    @staticmethod
    def refine(value, default=''):
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except:
                return default
