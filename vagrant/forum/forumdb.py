# "Database code" for the DB Forum.

import datetime
import psycopg2

POSTS = [("This is the first post.", datetime.datetime.now())]

conn = psycopg2.connect("dbname=forum")

cursor = conn.cursor()

def get_posts():
  """Return all posts from the 'database', most recent first."""
  posts_selector = "select * from posts;"
  cursor.execute(posts_selector)
  posts_results = cursor.fetchall()
  conn.close()
  return posts_results

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  post_created = "insert into posts values(%s)", (content,);
  cursor.execute(post_created)
  conn.commit()
  conn.close()
  # POSTS.append((content, datetime.datetime.now()))


#things I got wrong the first time
## move connection variables into the methods so that it makes
##sense to open and close the connection inside the method itself

###make a DBNAME constant