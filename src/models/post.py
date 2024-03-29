from common.database import Database
import uuid
import datetime


class Post(object):

    def __init__(self, blog_id, title, content, author, date=datetime.datetime.utcnow(), _id=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self._id = uuid.uuid4().hex if _id is None else _id
        self.created_date = date

    def save_to_mongo(self):
        Database.insert(collection='posts', data=self.to_json())

    def to_json(self):
        return {
            '_id': self._id,
            'blog_id': self.blog_id,
            'author': self.author,
            'content': self.content,
            'title': self.title,
            'created_date': self.created_date
        }

    @classmethod
    def from_mongo(cls, post_id):
        post_data = Database.find_one(collection='posts', query={'_id': post_id})
        return cls(**post_data)

    @staticmethod
    def from_blog(blog_id):
        return [post for post in
                Database.find(collection='posts', query={'blog_id': blog_id})]
