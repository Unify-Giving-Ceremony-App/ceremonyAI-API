from flask import Blueprint, request, jsonify, g
from services.ceremony_service import CeremonyTypeService, CeremonyPlanService

ceremony_bp = Blueprint("ceremony", __name__)

@ceremony_bp.route("/ceremonytype", methods=["GET", "POST"])
def ceremony_type():
    """ API endpoint to manage ceremony types """
    if request.method == "GET":
        service = CeremonyTypeService(g.db_session)
        types = service.get_ceremony_types()
        return jsonify(types), 200
    
    elif request.method == "POST":
        data = request.get_json()
        name = data.get("name")
        if not name:
            return jsonify({"error": "Name is required"}), 400
        service = CeremonyTypeService(g.db_session)
        try:
            new_type = service.add_ceremony_type(name)
            return jsonify(new_type), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        

@ceremony_bp.route('/ceremonyplan', methods=['POST', 'GET'])
def ceremony_plan():
    if request.method == "POST":
        data = request.get_json()
        email = data.get('email')
        if not email:
            return jsonify({"error": "user email is required"}), 400
        service = CeremonyPlanService(g.db_session)
        try:
            new_plan = service.add_ceremony_plan(email=email,ceremony_type=data.get('ceremony_type'),ceremony_metadata=data.get('ceremony_metadata'),voice_type=data.get('voice_type'),background_sound=data.get('background_sound'),ceremonial_companion=data.get('ceremonial_companion'),ceremony_duration=data.get('ceremony_duration'),meditation_duration=data.get('meditation_duration'),ceremony_prompts=data.get('ceremony_prompts'),meditation_prompts=data.get('meditation_prompts'),ceremony_datetime=data.get('ceremony_datetime'),participants=data.get('participants'))
            return jsonify(new_plan), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    
    elif request.method == "GET":
        service = CeremonyPlanService(g.db_session)
        plans = service.get_all_ceremony_plan()
        if not plans:
            return jsonify({'error': 'No ceremonies found'}), 404
        return jsonify(plans), 200


@ceremony_bp.route('/ceremonyplan/<int:ceremony_id>', methods=['GET', 'DELETE'])
def ceremony_plan_by_id(ceremony_id):
    service = CeremonyPlanService(g.db_session)
    if request.method == 'GET':
        plan = service.get_ceremony_plan_by_id(ceremony_id)
        if not plan:
            return jsonify({'error': 'Ceremony not found'}), 404
        return jsonify(plan), 200
    
    elif request.method == 'DELETE':
        success = service.delete_ceremony_plan_by_id(ceremony_id)
        if not success:
            return jsonify({'error': 'Ceremony not found'}), 404
        return jsonify({'message': 'Ceremony deleted'}), 200


@ceremony_bp.route('/user/ceremonyplan', methods=['GET'])
def user_ceremony_plans():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Email query parameter is required"}), 400
    service = CeremonyPlanService(g.db_session)
    try:
        plans = service.user_ceremony_plans(email)
        if not plans:
            return jsonify({'error': 'No ceremonies found for this user'}), 404
        return jsonify(plans), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404