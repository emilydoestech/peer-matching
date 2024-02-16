from flask import Flask
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config.update(
    TESTING=True,
    SECRET_KEY='327718c2f51ee911a084546121d03034'
)

# SESSION_TYPE = 'filesystem'
#
# sess = Session()
# sess.init_app(app)

from patientmatching import routes
