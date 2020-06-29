import scrapy

from op_gg.items import Summoner, SummonerChampion
from op_gg.lib.connection import Connection


class OpGgSpider(scrapy.Spider):
    name = "op_gg"

    url_summoner = 'https://www.op.gg/summoner/userName={name}'
    url_summoner_champion = 'https://www.op.gg/summoner/champions/userName={name}'

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(OpGgSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider.spider_opened()
        return spider

    def spider_opened(self):
        self.connector = Connection()

    def start_requests(self):
        while self.connector.queue:
            name = self.connector.queue.popleft()
            yield scrapy.Request(
                url=self.url_summoner.format(name=name),
                meta={'name': name},
                callback=self.parse_summoner)

    def parse_summoner(self, response):
        def _extract_info(node):
            def _rank_to_mmr(rank):
                ranks = ['Iron', 'Bronze', 'Silver', 'Gold', 'Platinum',
                        'Diamond', 'Master', 'Grandmaster', 'Challenger']
                rank_name, *rank_index = rank.split(' ')
                rank_index, *_ = rank_index or (0,)

                # Ignore GrandMaster and Challenger index
                return (min(ranks.index(rank_name), 6) + 1) * 400 - int(rank_index) * 100

            try:
                rank = node.xpath('//div[@class="TierRank"]/text()').get().strip()
            except AttributeError:
                return 0, 0, 0

            # Ignore Unranked
            if rank == 'Unranked':
                return 0, 0, 0

            rank_points, *_ = node.xpath('//span[@class="LeaguePoints"]/text()').get().split(' ')
            wins = int(node.xpath('//span[@class="wins"]/text()').get()[:-1])
            losses = int(node.xpath('//span[@class="losses"]/text()').get()[:-1])
            mmr = _rank_to_mmr(rank) + int(rank_points)

            return mmr, wins, losses

        summoner = Summoner(name=response.meta['name'])
        summoner['domain'] = self.name
        summoner['domain_id'] = response.xpath(
            '//div[@class="GameListContainer"]/@data-summoner-id').get()

        summoner['mmr'], summoner['wins'], summoner['losses'] = \
            _extract_info(response.xpath(
                '//div[@class="SummonerRatingMedium"]'))

        summoner['played_with'] = set(response.xpath(
            '//div[@class="SummonerName"]/a/text()').extract())

        yield summoner
        yield scrapy.Request(
            url=self.url_summoner_champion.format(name=response.meta['name']),
            meta=response.meta,
            callback=self.parse_summoner_champion)
            
    def parse_summoner_champion(self, response):
        def _refine(value, default=0):
            value = value.replace(',', '')
            try:
                return int(value)
            except ValueError:
                try:
                    return float(value)
                except:
                    return default

        for node in response.xpath('//tr[contains(@class, "Row")]')[1:]:
            champion = SummonerChampion(summoner=response.meta['name'])
            champion['name'] = node.xpath(
                './/td[contains(@class, "ChampionName")]/a/text()').get().strip()
            
            champion['wins'] = int((node.xpath(
                './/div[contains(@class, "Text Left")]/text()').get() or '0W')[:-1])
            champion['losses'] = int((node.xpath(
                './/div[contains(@class, "Text Right")]/text()').get() or '0L')[:-1])
            champion['kda'] = tuple(map(float, node.xpath(
                './/div[contains(@class, "KDA")]/span/text()').extract()))

            try:
                (   # deconstruct
                    champion['gold'],
                    champion['cs'],
                    champion['max_kill'],
                    champion['max_death'],
                    champion['add'],
                    champion['adt'],
                    champion['double_kill'],
                    champion['triple_kill'],
                    champion['quadra_kill'],
                    champion['penta_kill']
                ) = map(_refine, map(str.strip, node.xpath(
                    './/td[contains(@class, "Value Cell")]/text()').extract()))
            except ValueError:
                # case of no-rank, only normal
                pass

            yield champion
