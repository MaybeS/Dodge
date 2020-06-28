# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from op_gg.items import Summoner, SummonerChampion


class OpGgPipeline:
    def process_item(self, item, spider):
        for item_class, process in {
            Summoner: self.process_summoner,
            SummonerChampion: self.process_summoner_champion,
        }.items():
            if isinstance(item, item_class):
                process(item, spider.connector)
                break

    def process_summoner(self, item, connector):
        connector.queue.extend(item['played_with'])
        connector.commit()

        data = dict(item)
        data.pop('played_with', None)
        connector.set_summoner(item['name'], data)

    def process_summoner_champion(self, item, connector):
        data = dict(item)
        connector.set_summoner_champion(item['summoner'], item['name'], data)
