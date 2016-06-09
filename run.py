from stats import app
from stats import db

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
