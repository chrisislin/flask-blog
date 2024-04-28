# Documentation

### Deployment details

For deployment locally:
1. pip install -r requirements.txt
2. python3 main.py
3. Click on the link created, typically "http://127.0.0.1:5000/" for localhost

### Basic User Instructions

There's a login that needs to be used to interact with the blog, otherwise it redirects to the login, which will be our basic authentication.
The login can be logged in with username = "user" and password = "pass".
The blog aspects works as intended with all the blog features like create new blog post, retrieve list of all blog post, single post, update, and deleting a blog post.
The database is used with sqlite3. There are some unit tests, but they are very rudimentary as I didn't feel like I could implement them properly with the time I have.

### Tradeoff and designs
Some additional features that could be improved upon were more stringent unit tests. I didn't make as rigours tests as I would have liked. 
The login frontend could use more work and the authentication could be based on either a function or class than checking the authentication for each endpoint.
Otherwise, it is a simple blog.
