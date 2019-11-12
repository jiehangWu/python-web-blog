from common.database import Database
from src.models.blog import Blog


class Menu(object):

    def __init__(self):
        self.user = input("Enter name of author: ")
        self.user_blog = None
        if self._user_has_account():
            print("Welcome back {}".format(self.user))
        else:
            self._prompt_user_for_account()

    def _prompt_user_for_account(self):
        title = input("Enter blog title: ")
        description = input("Enter blog description")
        blog = Blog(author=self.user,
                    title=title,
                    description=description)
        blog.save_to_mongo()
        self.user_blog = blog

    def _user_has_account(self):
        blog = Database.find_one(collection='blogs', query={'author': self.user})
        if blog is not None:
            self.user_blog = Blog.from_mongo(blog['_id'])
            return True
        return False

    def run_menu(self):
        read_or_write = input("Do you want to read(R) of write(W) blogs")
        if read_or_write == 'R':
            self._list_blogs()
            self._view_blog()
        elif read_or_write == 'W':
            self._prompt_write_post()
        else:
            print("Thank you")

    def _prompt_write_post(self):
        self.user_blog.new_post()

    def _list_blogs(self):
        blogs = Database.find(collection='blogs', query={})
        for blog in blogs:
            print("ID: {}, Title: {}, Author: {}".format(blog['_id'], blog['title'], blog['author']))

    def _view_blog(self):
        id_blog_to_view = input('Enter the ID of the blog')
        blog = Blog.from_mongo(id_blog_to_view)
        posts = blog.get_posts()
        for post in posts:
            print("Date: {}, title: {}\n\n{}".format(post['created_date'], post['title'], post['content']))
