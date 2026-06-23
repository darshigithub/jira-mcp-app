from flask import Blueprint, jsonify
from models.project import JiraProject
from services.project_sync import ProjectSync

project_bp = Blueprint("project", __name__)

@project_bp.route("/projects")
def projects():

    data = JiraProject.query.all()

    return [
        {
            "key": p.project_key,
            "name": p.project_name
        }
        for p in data
    ]

@project_bp.route("/sync/projects", methods=["GET"])
def sync_projects():

    result = ProjectSync().sync()

    return jsonify(result)