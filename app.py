from flask import (
	Flask, render_template, request, redirect, url_for
)
import json
import os

# Define the file path for storing blog posts
JSON_FILE = 'posts.json'
app = Flask(__name__)

def load_posts():
	"""
	Loads blog post data from the JSON file.
	Initializes the file with an empty list if it does not exist.
	Returns:
		list: A list of dictionaries, each representing a blog post.
	"""
	if not os.path.exists(JSON_FILE):
		# Initialize file with an empty list if it doesn't exist
		with open(JSON_FILE, 'w') as f:
			json.dump([], f)
		return []

	with open(JSON_FILE, 'r') as f:
		# Load and return the list of posts
		return json.load(f)


def save_posts(posts):
	"""
	Saves the list of blog posts back to the JSON file.
	"""
	with open(JSON_FILE, 'w') as f:
		json.dump(posts, f, indent=4)


def initialize_posts():
	"""
	Initializes the posts.json file with sample data if it's empty.
	"""
	posts = load_posts()
	if not posts:
		sample_posts = [
			{"id": 1, "author": "John Doe",
			 "title": "First Post on Flask",
			 "content": "This is my first post, detailing the Flask setup.",
			 "likes": 0},
			{"id": 2, "author": "Jane Doe",
			 "title": "The Power of JSON",
			 "content": "This post explains why we use JSON for "
						"simple data storage.",
			 "likes": 0}
		]
		# Use the save_posts function to write initial data
		save_posts(sample_posts)
		print(f"Initialized {JSON_FILE} with sample data.")

@app.route('/')
def index():
	"""
	The index route, displaying all blog posts loaded from the JSON file.
	Returns:
		Rendered HTML template with the list of posts.
	"""
	blog_posts = load_posts()
	return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
	"""
	Handles both displaying the post creation form (GET) and
	processing the form submission (POST).
	Returns:
		Rendered HTML template for the add form or a redirect.
	"""
	if request.method == 'POST':
		posts = load_posts()

		# Generate a unique ID: use the ID of the last post + 1, or 1
		new_id = posts[-1]['id'] + 1 if posts else 1

		new_post = {
			"id": new_id,
			"author": request.form.get('author'),
			"title": request.form.get('title'),
			"content": request.form.get('content'),
			"likes": 0  # Initialize new post with 0 likes
		}

		posts.append(new_post)
		save_posts(posts)

		# Redirect the user back to the index page ('/')
		return redirect(url_for('index'))

	# For GET requests, render the form template
	return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
	"""
	Deletes a blog post specified by post_id and redirects to index.
	Returns:
	   A redirect response to the index page.
	"""
	posts = load_posts()

	# Filter out the post with the matching ID
	posts = [post for post in posts if post['id'] != post_id]

	save_posts(posts)

	return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
	"""
	Handles displaying the edit form (GET) and updating the post (POST).
	Returns:
	   Rendered HTML template for the edit form or a redirect.
	"""
	posts = load_posts()

	# Find the post by ID
	post_to_edit = next(
		(post for post in posts if post['id'] == post_id), None)

	# Simple error handling if post is not found
	if post_to_edit is None:
		return "Post not found", 404

	if request.method == 'POST':
		# Update the found post with data from the form
		post_to_edit['author'] = request.form.get('author')
		post_to_edit['title'] = request.form.get('title')
		post_to_edit['content'] = request.form.get('content')

		save_posts(posts)

		return redirect(url_for('index'))

	# For GET requests, render the form, passing the found post data
	return render_template('update.html', post=post_to_edit)


@app.route('/like/<int:post_id>')
def like(post_id):
	"""
	Increments the 'likes' count for the specified post and redirects to index.
	Returns:
		A redirect response to the index page.
	"""
	posts = load_posts()

	# Search the posts for the matching post
	for post in posts:
		if post['id'] == post_id:
			post['likes'] += 1
			break

	save_posts(posts)

	return redirect(url_for('index'))


if __name__ == '__main__':
	# Ensure the JSON file exists and has some initial data for testing
	initialize_posts()
	app.run(host="0.0.0.0", port=5000, debug=True)