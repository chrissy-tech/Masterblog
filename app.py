from flask import Flask, render_template, request, redirect, url_for # <-- ADDED redirect, url_for
import json
import os

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

# Define the file path for storing blog posts
JSON_FILE = 'posts.json'
app = Flask(__name__)

# ----------------------------------------------------------------------
# Data Handling Functions
# ----------------------------------------------------------------------

def load_posts():
    """
    Loads blog post data from the JSON_FILE.

    If the file does not exist, it initializes it with an empty list
    and returns an empty list.

    Returns:
        list: A list of dictionaries, where each dictionary represents a blog post.
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
    Saves the list of blog posts back to the JSON_FILE.

    Args:
        posts (list): The list of post dictionaries to save.
    """
    with open(JSON_FILE, 'w') as f:
        json.dump(posts, f, indent=4)

# Optional: Initialize the file with sample data if it's currently empty
def initialize_posts():
    """
    Initializes the posts.json file with sample data if it's empty.
    """
    posts = load_posts()
    if not posts:
        sample_posts = [
            {"id": 1, "author": "John Doe",
             "title": "First Post on Flask",
             "content": "This is my first post, detailing the Flask setup."},
            {"id": 2, "author": "Jane Doe",
             "title": "The Power of JSON",
             "content": "This post explains"
                        " why we use JSON for simple data storage."}
        ]
        save_posts(sample_posts)  # Use the new save_posts function
        print(f"Initialized {JSON_FILE} with sample data.")
# ----------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------

@app.route('/')
def index(): #<-- NEW INDEX ROUTE
    """
    The index route, displaying all blog posts loaded from the JSON file.

    Returns:
        Rendered HTML template with the list of posts.
    """
    # 1. Fetch all blog posts using the data handling function
    blog_posts = load_posts()

    # 2. Render the index.html template and pass the list of posts
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])  # <-- NEW ROUTE
def add():
    """
    Handles both displaying the post creation form (GET) and
    processing the form submission (POST).

    Returns:
        Rendered HTML template for the add form.
    """
    if request.method == 'POST':
        # 1. Fetch current posts list
        posts = load_posts()

        # 2. Generate a unique ID: use the ID of the last post + 1, or 1 if the list is empty
        new_id = posts[-1]['id'] + 1 if posts else 1

        # 3. Get data from the form (using the 'name' attributes from add.html)
        new_post = {
            "id": new_id,
            "author": request.form.get('author'),
            "title": request.form.get('title'),
            "content": request.form.get('content')
        }

        # 4. Add the new post and save the updated list
        posts.append(new_post)
        save_posts(posts)

        # 5. Redirect the user back to the index page ('/')
        return redirect(url_for('index'))

    # For GET requests, render the form template
    return render_template('add.html')


if __name__ == '__main__':
    # Ensure the JSON file exists and has some initial data for testing
    initialize_posts()
    app.run(host="0.0.0.0", port=5001, debug=True)
