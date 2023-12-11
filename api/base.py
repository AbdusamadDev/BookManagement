from authentication import auth_route
from flask import Flask

app = Flask(__name__)
app.register_blueprint(auth_route, )

app.get("/test")


def testing(request):
    return "Test"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, use_reloader=True)
