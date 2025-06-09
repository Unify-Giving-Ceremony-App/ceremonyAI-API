from flask import Blueprint, jsonify, request
from services.notification_service import NotificationService

notification_bp = Blueprint("notification", __name__)

@notification_bp.route("/notify", methods=["POST"])
def send_notification():
    """ API endpoint to send notifications """
    data = request.get_json()
    user_id = data.get("user_id")
    message = data.get("message")

    if not user_id or not message:
        return jsonify({"error": "user_id and message are required"}), 400

    # Enqueue the notification task
    task = NotificationService.send_notification_task(user_id, message)
    return jsonify({"task_id": task.id, "status": "Notification is being sent"}), 202

@notification_bp.route("/status/<task_id>", methods=["GET"])
def get_status(task_id):
    """ API endpoint to check the status of a notification """
    task = NotificationService.send_notification_task.AsyncResult(task_id)
    if task.state == "PENDING":
        response = {"state": task.state, "status": "Pending..."}
    elif task.state != "FAILURE":
        response = {"state": task.state, "status": task.info.get("status", "")}
        if task.result:
            response["result"] = task.result
    else:
        # Something went wrong in the background job
        response = {"state": task.state, "status": str(task.info)}
    return jsonify(response)
