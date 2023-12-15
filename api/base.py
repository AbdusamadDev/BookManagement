from flask import Flask
from user_profiles import auth_route
from bms import bms_route

app = Flask(__name__)
app.register_blueprint(auth_route)
app.register_blueprint(bms_route)


@app.get("/")
def testing():
    return "HomePage"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
