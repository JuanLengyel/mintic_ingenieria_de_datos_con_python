import logging
logging.basicConfig(level=logging.INFO)
import subprocess


logger = logging.getLogger(__name__)
<<<<<<< HEAD
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

=======
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
>>>>>>> 0947655875ed10fe36e96916e3a4da86cb1b43f4

if __name__ == "__main__":
    main()