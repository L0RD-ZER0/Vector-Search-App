from libs import sql
from random import randint
from json import dump


MAX_INDEX = 12261


def make_sample():
    ids = set()
    while len(ids) < 6:
        ids.add(1 + randint(0, MAX_INDEX))
    ids = list(ids)
    articles = sql.query_articles(ids)
    art = {
        'id': MAX_INDEX + 1,
        'title': articles[0]['title'],
        'authors': articles[1]['authors'],
        'affiliations': articles[2]['affiliations'],
        'abstract': articles[3]['abstract'],
        'text': articles[4]['text'],
        'bibliography': articles[5]['bibliography'],
    }
    string = art['title'] + '\n\n' + '=' * 20 + '\n\n' + art['text']
    with open(f"./data/{ids[0]}-{ids[4]}.json", 'w') as f:
        dump(art, f)
    with open(f"./data/{ids[0]}-{ids[4]}.txt", 'wb') as f:
        f.write(string.encode('utf-8'))


def make_samples(count: int = 5):
    for _ in range(count):
        make_sample()
        print(f'{_+1} / {count} done.')


if __name__ == '__main__':
    sql.init_mysql()
    make_samples()
    sql.teardown_mysql()
