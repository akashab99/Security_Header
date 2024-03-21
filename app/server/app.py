# Creates a Base files to run the Application
from flask import Flask

# Internal Imports
from route.search import search_page

app = Flask(__name__)

# Register the blueprint with the app
app.register_blueprint(search_page)

if __name__ == "__main__":
    app.run(debug=True)
