# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Summoner(scrapy.Item):
    def __repr__(self):
        return f'Summoner: {self["name"]}'

    name = scrapy.Field()

    domain = scrapy.Field()
    domain_id = scrapy.Field()
    mmr = scrapy.Field()
    wins = scrapy.Field()
    losses = scrapy.Field()
    played_with = scrapy.Field()
    champions = scrapy.Field()
    

class SummonerChampion(scrapy.Item):
    def __repr__(self):
        return f'Summoner: {self["summoner"]} Champion: {self["name"]}'

    summoner = scrapy.Field()
    name = scrapy.Field()

    wins = scrapy.Field()
    losses = scrapy.Field()
    kda = scrapy.Field()
    gold = scrapy.Field()
    cs = scrapy.Field()
    max_kill = scrapy.Field()
    max_death = scrapy.Field()
    add = scrapy.Field()
    adt = scrapy.Field()
    double_kill = scrapy.Field()
    triple_kill = scrapy.Field()
    quadra_kill = scrapy.Field()
    penta_kill = scrapy.Field()
