import argparse
import logging
logging.basicConfig(level=logging.INFO)
from urllib.parse import urlparse

import pandas as pd


logger = logging.getLogger(__name__)

def main(filename):
    logger.info('Starting cleaning process')

    df = _read_data(filename)
    newspaper_uid = _extract_newspaper_uid(filename)

    df = _add_newspaper_uid_column(df, newspaper_uid)
    df = _extract_host(df)

    return df

def _read_data(filename):
    logger.info('Reading data from file {}'.format(filename))

    return pd.read_csv(filename)

def _extract_newspaper_uid(filename):
    logger.info('Extracting newspaper uid from file {}'.format(filename))

    return filename.split('_')[0]

def _add_newspaper_uid_column(df, newspaper_uid):
    logger.info('Filling column uid with newspaper uid {}'.format(newspaper_uid))

    df['newspaper_uid'] = newspaper_uid
    return df

def _extract_host(df):
    logger.info('Extracting host from urls')

    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)
    return df


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='Path to dirty data',
                        type=str)

    args = parser.parse_args()

    df = main(args.filename)

    print(df)