import sqlite3
from models import Article

"""
These functions perform the pushing and getting of data from the database.

articles.db TABLE DEFFINITIONS
TABLE articles
    COLUMNS (
        id INTEGER PRIMARY KEY,
        title TEXT,
        body TEXT,
        date TEXT,
    )

TABLE tags
    COLUMNS (
        row_id INTEGER PRIMARY KEY,
        article_id INTEGER,
        tagName TEXT,
        UNIQUE (article_id, tagName)
    )

"""

def add_article(article):
    """take an article object and add it to the articles.db

    :param article:  an articles object of type models.Article
    :returns: Boolean True if successful
    """
    connection = sqlite3.connect('articles.db')
    cursor = connection.cursor()
    
    cursor.execute("INSERT OR REPLACE INTO articles VALUES (:id, :title, :body, :date)",
        {'id': article.id, 'title': article.title, 'body': article.body, 'date': article.date })
    connection.commit()
    for tag in article.tags:
        cursor.execute("""INSERT OR IGNORE INTO tags (article_id, tagName) VALUES (:article_id, :tagName);""",
                            {'article_id': article.id, 'tagName': tag})
        connection.commit()
    connection.close()
    return True

def get_article(id):
    """use an id to search the articles.db

    :param id:  type int
    :returns: models.Article Object or None if not found.
    """
    connection = sqlite3.connect('articles.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM articles WHERE id=(:id)", {'id': id})
    tup = cursor.fetchone()
    if tup is None:
        return None
    article = Article(tup[0],tup[1], tup[2], tup[3])
    cursor.execute("SELECT tagName FROM tags WHERE article_id=(:article_id)", {'article_id': id})
    tags = clean_list_tuple(cursor.fetchall())
    article.set_tags(tags)
    connection.close()
    return article

def get_tag_data(tag, date):
    """Searches the database for occurences of a tag on a given date and
    gets the total count of occurances, article_ids of articles with the tags on the date,
    and related tags used on the same articles.

    :param tag: String of a tagName
    :param date: date_string in format yyyy-mm-dd
    :returns: Dictionary with keys [tag, count, articles, related_tags]
    """
    # Design spec says:
    # "The articles field contains a list of ids for the last 10 articles entered for that day."
    # However, there is no time stamp assoicated with the article.date. We can truncate to 10 articles
    # with no sort order or report all article_ids. For now, the latter option has been chosen.

    connection = sqlite3.connect('articles.db')
    cursor = connection.cursor()

    cursor.execute("""SELECT article_id FROM tags
                         WHERE tagName=(:tagName)
                         AND article_id IN
                         (SELECT id FROM articles WHERE date=(:date))""",
                     {'tagName': tag, 'date': date})

    article_ids = clean_list_tuple(cursor.fetchall())
    
    # No need to continue if there are no article ID's
    if len(article_ids) == 0:
        return {'tag': tag, 'count': 0, 'articles': [], 'related_tags': []}
    
    cursor.execute("""SELECT tagName FROM tags WHERE tagName!=(:tagName)
                        AND article_id IN
                        (SELECT article_id FROM tags
                         WHERE tagName=(:tagName)
                         AND article_id IN
                         (SELECT id FROM articles WHERE date=(:date)))""",
                     {'tagName': tag, 'date': date})

    related_tags = clean_list_tuple(cursor.fetchall())
    
    #remove duplicate related tags
    related_tags = list(dict.fromkeys(related_tags))
    count = len(article_ids)
    
    connection.close()

    return {'tag': tag, 'count': count, 'articles': article_ids, 'related_tags': related_tags}



def clean_list_tuple(list_):
    """
    helper function becasue sqlite returns a list where each row from the db
    is in a tuple. this function pulls the item out of single tuples.
    """
    output = []
    if list_ is not None:
        for item in list_:
            output.append(str(item[0]))
    return output