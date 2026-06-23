from flask import Flask

from config import Config
from database.db import db

from routes.project_routes import project_bp
from routes.issue_routes import issue_bp
from routes.dashboard_routes import dashboard_bp
from routes.comment_routes import comment_bp
from routes.histroy_routes import history_bp

from scheduler.jobs import init_scheduler


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

# Start scheduler AFTER app is created
init_scheduler(app)


@app.route("/")
def home():
    return {
        "status": "running"
    }


if __name__ == "__main__":
    app.run(debug=True)