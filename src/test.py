from common.database import Database
from models.post import Post

Database.initialize()
print(Database.DATABASE)
print(Database.DATABASE['posts'])
print(Post.from_blog("2"))
