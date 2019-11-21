import argparse
import logging
logging.basicConfig(level=logging.INFO)

import pandas as pd

from article import Article
from base import Base, engine, Session

logger = logging.getLogger(__name__)

def main(filename):
    Base.metadata.create_all(engine)
    session = Session()
    article = pd.read_csv(filename)

    for index, row in article.iterrows():
        logger.info('Loading article uid {} into DB'.format(row['uid']))

        article = Article(row['uid'],
                          row['body'],
                          row['host'],
                          row['title'],
                          row['newspaper_uid'],
                          row['n_token_body'],
                          row['n_token_title'],
                          row['url'])

        session.add(article)
    
    session.commit()
    session.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='The file to load into db',
                        type=str)

    args = parser.parse_args()

    main(args.filename)