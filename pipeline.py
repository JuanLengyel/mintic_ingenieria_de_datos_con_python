import logging
logging.basicConfig(level=logging.INFO)
import subprocess


logger = logging.getLogger(__name__)
news_paper_uids = ['semana', 'eltiempo']

def _extract():
    logger.info('Starting extract process')

    for news_paper_uid in news_paper_uids:
        subprocess.run(['python', 'main.py', news_paper_uid], cwd='./web_scrapper')
        subprocess.run(['move', '{}*.csv'.format(news_paper_uid), '../newspaper_recipe/{}_.csv'.format(news_paper_uid)], cwd='./web_scrapper', shell=True)

def _transform():
    logger.info('Starting transform process')
    
    for news_paper_uid in news_paper_uids:
        dirty_data_filename = '{}_.csv'.format(news_paper_uid)
        clean_data_filename = 'clean_{}'.format(dirty_data_filename)

        subprocess.run(['python', 'newspaper_recipe.py', dirty_data_filename], cwd='./newspaper_recipe')
        subprocess.run(['del', dirty_data_filename], cwd='./newspaper_recipe', shell=True)
        subprocess.run(['move', clean_data_filename, '../dataSystem/'], cwd='./newspaper_recipe', shell=True)       

def _load():
    logger.info('Starting load process')
    
    for news_paper_uid in news_paper_uids:
        subprocess.run(['python', 'main.py', 'clean_{}_.csv'.format(news_paper_uid)], cwd='./dataSystem')
        subprocess.run(['del', 'clean_{}_.csv'.format(news_paper_uid)], cwd='./dataSystem', shell=True)

def main():
    _extract()
    _transform()
    _load()

if __name__ == "__main__":
    main()