import datetime
import db_interface

from flask import Flask, jsonify, request, render_template
from models import Article


def main():
    """
    main method which runs the Flask server, declares the paths and API endpoints.
    """
    app = Flask(__name__)

    @app.route('/')
    def home():
        return render_template('index.html')

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
                new_article = Article(article['id'], article['title'], article['body'], article['date'], [])
            except Exception as e:
                return str(e), 400

            for tag in article['tags']:
                new_article.add_tag(tag)
            
            db_interface.add_article(new_article)
            return f'Sucessfully added article to the database:\n{str(new_article)}', 201


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
            if len(date) == 8:
                date_text = f'{date[:4]}-{date[4:6]}-{date[6:]}'
                try:
                    date_time = datetime.datetime.strptime(date_text, '%Y-%m-%d')
                    date = str(datetime.datetime.date(date_time))
                except ValueError:
                    return f"""Could not cast cast {date_text} to a real date.
                                Ensure date paramter is a real date and in the format YYYYMMDD""", 400
            else:
                return "Incorrect data format, should be YYYYMMDD", 400
            return jsonify(db_interface.get_tag_data(tagName, date))

    app.run()

if __name__ == '__main__':
    main()