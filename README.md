# Time to dodge!


## Redis for crawling summoners statics

Redis structer
```
champion:{champion_name}
summoner:{summoner_name}
summoner-champion-{summoner_name}:{champion_name} # related on summoner

crawl-queue # store pending list
```
