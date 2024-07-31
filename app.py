from flask import Flask

import routes

app = Flask(__name__)

# Register all routes from routes.py
routes.register_routes(app)

if __name__ == "__main__":
   app.run(port=8000, debug=True)
