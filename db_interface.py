from calendar import c
import sqlite3
from models import Article


connection = sqlite3.connect('articles.db')
cursor = connection.cursor()

"""
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
        id INTEGER PRIMARY KEY,
        article_id INTEGER,
        tagName TEXT
    )

"""

def add_article(article):
    """take an article object and add it to the articles.db

    :param article:  an articles object of type models.Article
    :returns: Boolean True if successful
    """
    connection = sqlite3.connect('articles.db')
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO articles VALUES (:id, :title, :body, :date)",
        {'id': article.id, 'title': article.title, 'body': article.body, 'date': article.date })
    connection.commit()
    for tag in article.tags:
        cursor.execute("INSERT INTO tags VALUES (:article_id, :tagName)", {'article_id': article.id, 'tagName': tag})
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
    connection = sqlite3.connect('articles.db')
    cursor = connection.cursor()

    #query for article ids with matching date
    cursor.execute("SELECT id FROM articles WHERE date=(:date)", {'date': date})
    date_article_ids = clean_list_tuple(cursor.fetchall())
    if date_article_ids is None: return None 
    #query for article ids with matching tag and date
    cursor.execute("SELECT article_id FROM tags WHERE tagName=(:tagName) AND article_id IN (:article_ids)", {'tagName': tag, 'article_ids': date_article_ids})
    tag_article_ids = clean_list_tuple(cursor.fetchall())
    if tag_article_ids is None: return None
    #sum of articles with matching tag and date
    count = len(tag_article_ids)
    #query for related tags
    cursor.execute("SELECT tagName FROM tags WHERE tagName!=(:tagName) AND article_id IN (:article_ids)", {'tagName': tag, 'article_ids': tag_article_ids })
    related_tags = clean_list_tuple(cursor.fetchall())
    if related_tags:
        related_tags = []
    else:
        related_tags = list(dict.fromkeys(related_tags))
    
    connection.close()

    return {'tag': tag, 'count': count, 'articles': tag_article_ids, 'related_tags': related_tags}



def clean_list_tuple(list_):
    """
    helper function becasue sqlite returns a list where each row from the db
    is in a tuple. this function pulls the item out of single tuples.
    """
    output = []
    if list_:
        if len(list_) > 0:
            if len(list[0]) == 1:
                for item in list_:
                    output += item[0]
    return output
                    
connection.commit()
connection.close()