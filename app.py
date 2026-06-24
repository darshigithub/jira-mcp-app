from flask import Flask, jsonify

from config import Config
from database.db import db

from routes.project_routes import project_bp
from routes.issue_routes import issue_bp
from routes.dashboard_routes import dashboard_bp
from routes.comment_routes import comment_bp
from routes.histroy_routes import history_bp

from services.sync_all import SyncAll


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(project_bp)
app.register_blueprint(issue_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(comment_bp)
app.register_blueprint(history_bp)

@app.route("/")
def home():
    return {
        "status": "running"
    }

# sync/all endpoint to sync all the service data into sqllite DB
@app.route("/sync/all")
def sync_all():

    result = SyncAll().sync()

    return jsonify(result)


if __name__ == "__main__":

    app.run(
        debug=True,
        use_reloader=False
    )
