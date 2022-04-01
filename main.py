import db_interface

from flask import Flask, jsonify, request
from models import Article
def main():
    """
    main method which runs the Flask server, declares the paths and API endpoints.
    """
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
            article = request.get_json(silent=True)
            keys = article.keys()
            expected_keys = ['id', 'title', 'body', 'date', 'tags']

            for key in expected_keys:
                if key not in keys:
                    return f"expected request body to have key: {key}, but was not found.", 400

            try:
                new_article = Article(article['id'], article['title'], article['body'], article['date'])
            except Exception as e:
                return str(e), 400

            for tag in article['tags']:
                new_article.add_tag(tag)
            
            db_interface.add_article(new_article)
            return f'Sucessfully added article to the database: {str(new_article)}', 201


    @app.route('/articles/<id>', methods=['GET'])
    def get_article(id):
        if request.method == 'GET':
            article = db_interface.get_article(id)
            if article is not None:
                article_dict = article.to_dictionary()
                return jsonify(article_dict)
            else:
                return 'No matching article found.', 404

    @app.route('/tags/<tagName>/<date>', methods=['GET'])
    def get_tag_data_on_date(tagName, date):
        if request.method == 'GET':
            return jsonify(db_interface.get_tag_data(tagName, date))

    app.run()

if __name__ == '__main__':
    main()