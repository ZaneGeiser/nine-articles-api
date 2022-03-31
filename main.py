import json
import sqlite3
import db_interface

from flask import Flask, jsonify, request
from models import Article
def main():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return """
        <h1>Welcome to a simple articles api.</h1>
        <h4>Available endpoints:</h4>
        <ul>
        <li>POST an article to path /article</li>
        <li>GET an article from /articles/{id}</li>
        <li>GET tag info from /tags/{tagName}/{date}</li>
        </ul>
        """

    @app.route('/articles', methods=['POST'])
    def post_article():
        if request.method == 'POST':
            article = request.get_json()
            print(article)
            keys = article.keys()
            expected_keys = ['id', 'title', 'body', 'date', 'tags']
            for key in expected_keys:
                if key not in keys:
                    return "Bad Request"
            new_article = Article(article['id'], article['title'], article['body'], article['date'], article['tags'])
            db_interface.add_article(new_article)
            return 'Success'


    @app.route('/articles/<id>', methods=['GET'])
    def get_article(id):
        if request.method == 'GET':
            article = db_interface.get_article(id)
            if article is not None:
                article_dict = {
                    'id': article.id,
                    'title': article.title,
                    'body': article.body,
                    'date': article.date,
                    'tags': article.tags
                }
                return jsonify(article_dict)
            else:
                return 'No matching article found.'

    @app.route('/tags/<tagName>/<date>', methods=['GET'])
    def get_tag_data_on_date(tagName, date):
        if request.method == 'GET':
            return jsonify(db_interface.get_tag_data(tagName, date))

    app.run()

    

if __name__ == '__main__':
    main()