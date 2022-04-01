import datetime

class Article():
    """
    Python Object to represent an article. used over simple python dictionary
    in order to abstract away some data validation.
    """
    def __init__(self, id, title, body, date, tags=[]):
        self.id = id
        self.title = title
        self.body = body
        self.set_date(date)
        self.set_tags(tags)

    def to_dictionary(self):
        return {
                    'id': self.id,
                    'title': self.title,
                    'body': self.body,
                    'date': self.date,
                    'tags': self.tags
                }

    def set_title(self, title):
        self.title = title
    
    def set_body(self, body):
        self.body = body
    
    def set_date(self, date_text):
        try:
            date_time = datetime.datetime.strptime(date_text, '%Y-%m-%d')
            self.date = str(datetime.datetime.date(date_time))
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        
    def set_tags(self, tags):
        if isinstance(tags, list):
            self.tags = tags
        else:
            try:
                self.tags = list(tags)
            except TypeError:
                raise TypeError('incorrect tags format. tags must be in a list.')
            
    def add_tag(self, tag):
        if isinstance(tag, str):
            self.tags.append(str(tag))
        print('tags after adding tags: ' + str(self.tags))
    
    def __str__(self):
        return f"""Article fields:
                    id: {self.id},
                    title: {self.title},
                    body: {self.body},
                    date: {self.date},
                    tags: {self.tags}"""
