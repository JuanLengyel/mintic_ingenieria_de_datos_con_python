import argparse
import hashlib
import logging
logging.basicConfig(level=logging.INFO)
from urllib.parse import urlparse

import pandas as pd
import nltk
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('spanish'))

logger = logging.getLogger(__name__)

def main(filename):
    logger.info('Starting cleaning process')

    df = _read_data(filename)
    newspaper_uid = _extract_newspaper_uid(filename)

    df = _add_newspaper_uid_column(df, newspaper_uid)
    df = _extract_host(df)
    df = _fill_missing_titles(df)
    df = _generate_uids_for_rows(df)
    df = _remove_new_lines_from_body(df)
    df = _tokenize_column(df, 'title')
    df = _tokenize_column(df, 'body')
    df = _remove_duplicate_entries(df, 'title')
    df = _drop_rows_with_missing_values(df)
    _save_data(df, filename)

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

def _fill_missing_titles(df):
    logger.info('Filling missing titles')

    missing_titles_mask = df['title'].isna()

    missing_titles = (df[missing_titles_mask]['url']
                        .str.extract(r'(?P<missing_titles>[^/]+)/[^/]+$')
                        .applymap(lambda title: title.split('-'))
                        .applymap(lambda title_word_list: ' '.join(title_word_list))
                    )

    df.loc[missing_titles_mask, 'title'] = missing_titles.loc[:, 'missing_titles']

    return df

def _generate_uids_for_rows(df):
    logger.info('Generating uids for each row')

    uids = (df
                .apply(lambda row: hashlib.md5(bytes(row['url'].encode())), axis=1)
                .apply(lambda hash_object: hash_object.hexdigest())
            )

    df['uid'] = uids
    return df.set_index('uid')

def _remove_new_lines_from_body(df):
    logger.info('Cleaning new lines from body')

    stripped_body = (df
                        .apply(lambda row: row['body'], axis=1)
                        .apply(lambda body: list(body))
                        .apply(lambda letters: list(map(lambda letter: letter.replace('\n',''), letters)))
                        .apply(lambda letters: ''.join(letters))
                    )

    df['body'] = stripped_body

    return df

def _tokenize_column(df, column_name):
    tokenized_column = (df
                            .dropna()
                            .apply(lambda row: nltk.word_tokenize(row[column_name]), axis=1)
                            .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens)))  
                            .apply(lambda tokens: list(map(lambda token: token.lower(), tokens)))
                            .apply(lambda words_list: list(filter(lambda word: word not in stop_words, words_list)))
                            .apply(lambda words_list: len(words_list))
                        )
    df['n_token_' + column_name] = tokenized_column

    return df

def _remove_duplicate_entries(df, column_name):
    logger.info('Removing duplicate entries')

    return df.drop_duplicates(subset=[column_name], keep='first')

def _drop_rows_with_missing_values(df):
    logger.info('Removing entries with missing values')

    return df.dropna()

def _save_data(df, filename):
    clean_filename = 'clean_{}'.format(filename)

    logger.info('Saving data at location {}'.format(clean_filename))

    df.to_csv(clean_filename)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='Path to dirty data',
                        type=str)

    args = parser.parse_args()

    df = main(args.filename)

    print(df)