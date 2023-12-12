from flask import Flask
from authentication import auth_route

app = Flask(__name__)
app.register_blueprint(auth_route, prefix="/auth")


@app.get("/test")
def testing():
    return "Test"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, use_reloader=True)
