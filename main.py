from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime

# Importing the logic from our separate service files
from preprocessing import DataPreprocessor
from ai_service import AIService
from cost_service import CostService
from resource_service import ResourceService
from schedule_service import ScheduleService
from utils import generate_project_id, get_current_timestamp

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
# Note: In a production environment, use environment variables for keys.
GEMINI_API_KEY = "AIzaSyApnF5WIEXeyzUzRZCISgpj7-8GXwIBgS8"

# Initialize Services
# We pass the API key to the AIService for external LLM calls
ai_service = AIService(api_key=GEMINI_API_KEY)
cost_service = CostService()
resource_service = ResourceService()
schedule_service = ScheduleService()

@app.route('/api/calculate', methods=['POST'])
def calculate_construction_plan():
    try:
        raw_data = request.json
        if not raw_data:
            return jsonify({"error": "No input data provided"}), 400

        # 1. Preprocessing & Validation
        # Standardizing inputs using the DataPreprocessor utility
        area = DataPreprocessor.validate_area(raw_data.get('built_up_area', 0))
        floors = DataPreprocessor.clean_floor_input(raw_data.get('floors', 'G+0'))
        
        # Ensure numeric values are properly cast to floats/ints
        try:
            daily_wage = float(raw_data.get('daily_wage_per_worker', 500))
            cost_per_sq_yard = float(raw_data.get('cost_per_sq_yard', 1500))
            user_days = raw_data.get('construction_days')
            if user_days is not None:
                user_days = int(user_days)
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid numeric input for wages, costs, or days"}), 400

        # 2. Schedule Generation
        sched_data = schedule_service.generate_schedule(area, floors, user_days)
        
        # 3. Resource & Labor Estimation
        materials = resource_service.calculate_materials(area, floors)
        labor = resource_service.calculate_labor(area, sched_data['duration_days'])
        
        # 4. Cost Calculation
        costs = cost_service.calculate_costs(
            area, 
            cost_per_sq_yard, 
            labor['total_labor_days'], 
            daily_wage
        )

        # 5. AI Insights & Blueprint Generation
        # The AIService now utilizes the provided API key for its logic
        blueprint_url = ai_service.generate_blueprint(floors, area)
        insights = ai_service.get_smart_insights(
            area, 
            costs['total_project_cost'], 
            sched_data['duration_weeks']
        )

        # 6. Assemble Final Response Object
        response = {
            "status": "success",
            "project_id": generate_project_id(),
            "timestamp": get_current_timestamp(),
            "timeline": {
                "duration_days": sched_data['duration_days'],
                "duration_weeks": sched_data['duration_weeks'],
                "duration_months": sched_data['duration_months']
            },
            "costs": costs,
            "materials": materials,
            "labor": labor,
            "schedule": sched_data['schedule'],
            "blueprints": [
                {
                    "floor_name": "Standard Layout",
                    "image_url": blueprint_url
                }
            ],
            "insights": insights
        }

        return jsonify(response), 200

    except Exception as e:
        # Logging the error for server-side debugging
        print(f"Error occurred: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint to verify backend status."""
    return jsonify({"status": "online", "model": "Gemini-Integrated-Granite"}), 200

if __name__ == '__main__':
    print("Construction AI Backend starting on http://127.0.0.1:5000")
    # debug=True allows for auto-reloading during development
    app.run(debug=True, port=5000)