import json
import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess

class GP_Posts_Spider(scrapy.Spider):
    name = 'gp_posts'

    start_urls = ['https://www.greenpeace.org/brasil/blog/?page=' + str(p) for p in range(1, 200)]

    def parse (self, response):
        for post in response.css('.d-flex.search-result-list-item'):
            if (post.css('.search-result-item-author ::text').get() == '\nGreenpeace Brasil\n') or (post.css('.search-result-item-author a::text').get() == 'Greenpeace Brasil'):
                yield response.follow(post.css('a.search-result-item-headline::attr(href)').get(), callback=self.parse_article)

    def parse_article (self, response):
        yield {
            'titulo' : response.css('.page-header-title::text').get(),
            'link' : response.request.url,
            'data' : response.css('.single-post-time::text').get(),
            'header' : response.css('.post-content-lead h4::text').get(),
            'texto' : response.css('.post-content-lead p ::text').getall()
        }
        
process = CrawlerProcess ({
    'FEED_FORMAT' : 'json',
    'FEED_URI' : 'posts_gp.json',
    'FEED_EXPORT_ENCODING' : 'utf-8'
})

process.crawl(GP_Posts_Spider)
process.start()

df = pd.read_json('posts_gp.json')

# Ajuste Datas

df = df[df['data'].notna()]

dict_mes = {
    'janeiro' : 1,
    'fevereiro' : 2,
    'março' : 3,
    'abril' : 4,
    'maio' : 5,
    'junho' : 6,
    'julho' : 7,
    'agosto' : 8,
    'setembro' : 9,
    'outubro' : 10,
    'novembro' : 11,
    'dezembro' : 12
}

df['day'] = df['data'].apply(lambda x: int(x.split(' de ')[0]))
df['month'] = df['data'].apply(lambda x: x.split(' de ')[1])
df['month'] = df['month'].map(dict_mes)
df['year'] = df['data'].apply(lambda x: int(x.split(' de ')[2]))
df['data_corr'] = pd.to_datetime(df[['year', 'month', 'day']])

# Ordenação das rows por data

df.sort_values(by='data_corr', inplace=True)

# Concatenação dos textos

df['texto'] = df['texto'].apply(lambda x: '\n'.join(x))



with open('./data/posts_greenpeace.txt','a+') as f:
    for index, row in df.iterrows():
        f.write('\n\n\nTítulo: %s\n' % row['titulo'])
        f.write('\nLink: %s\n' % row['link'])
        f.write('\nData: %s\n' % row['data'])
        f.write('\nHeader: \n %s\n' % row['header'])
        f.write('\nPost: \n %s' % row['texto'])

