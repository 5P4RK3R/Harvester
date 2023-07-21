from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from scrapy.crawler import CrawlerProcess
import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small.author::text').get(),
            }
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'harvester',
    default_args=default_args,
    schedule_interval='@daily',
)

def scrape_quotes():
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'FEED_FORMAT': 'csv',
        'FEED_URI': '/path/to/save/quotes.csv',
    })
    process.crawl(QuotesSpider)
    process.start()

scrape_task = PythonOperator(
    task_id='scrape_quotes',
    python_callable=scrape_quotes,
    dag=dag,
)

scrape_task
