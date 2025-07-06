from flask import Blueprint, request, jsonify, g
from services.newsletter_service import NewsletterService

newsletter_bp = Blueprint("newsletter", __name__)

@newsletter_bp.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required"}), 400
    newsletter_service = NewsletterService(g.db_session)
    try:
        newsletter_service.subscribe(email)
        return jsonify({"message": "Subscribed successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400