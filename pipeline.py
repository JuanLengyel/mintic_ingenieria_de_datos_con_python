import logging
logging.basicConfig(level=logging.INFO)
import subprocess


logger = logging.getLogger(__name__)
news_sites_uids = ['eltiempo', 'semana']

def main():
    _extract()
    _transform()
    _load()

def _extract():
    logger.info('Starting extraction process')
    for news_sites_uid in news_sites_uids:
        subprocess.run(['python', 'main.py', news_sites_uid], cwd='./web_scrapper')
        subprocess.run(['find', '.', '-name', '{}*'.format(news_sites_uid),
                        '-exec', 'mv', '{}', '../newspaper_recipe/{}_.csv'.format(news_sites_uid), ';'],
                        cwd='./web_scrapper')

def _transform():
    logger.info('Starting transformation process')

def _load():
    logger.info('Starting loading process')


if __name__ == "__main__":
    main()