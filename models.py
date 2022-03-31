import datetime

class Article():
    def __init__(self, id, title, body, date, tags=[]):
        self.id = id
        self.title = title
        self.body = body
        self.date = date
        self.tags = self.set_tags(tags)

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
