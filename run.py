from project.config import config
from project.server import create_app

app = create_app(config)


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
