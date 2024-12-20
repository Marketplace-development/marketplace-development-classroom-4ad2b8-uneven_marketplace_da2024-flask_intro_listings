# chat.py
from flask import Blueprint, request, jsonify, render_template

chat = Blueprint('chat', __name__)

# Predefined FAQ responses
FAQ_RESPONSES = {
    "list plant": "To list your plant, create an account, go to 'My Plants', and click 'Add Plant'. Provide details like care instructions and availability.",
    "become sitter": "Sign up as a plant sitter by creating a profile and setting your availability. You'll start receiving requests from plant owners nearby.",
    "pricing": "Pricing depends on the sitter's rates and the plant's care requirements. You can negotiate directly with the sitter.",
    "safety": "We verify all sitters through ID checks and reviews to ensure your plants are in safe hands.",
    "care details": "Provide specific care instructions for your plant, including watering frequency, sunlight needs, and any special requirements.",
    "payment": "Payments are processed securely through our platform. Owners pay upfront, and sitters receive payment after completing the job.",
    "cancelation": "You can cancel a booking up to 72 hours in advance for a full refund. After that, fees may apply.",
    "reviews": "Both owners and sitters can leave reviews after a booking. This helps build trust within our community.",
    "contact_support": "If you have any issues or questions, contact our support team at support@plantsitting.com for assistance.",
    "thank you": "You're welcome! I'm here to help anytime.",
    "default": "I'm sorry, I didn't understand that. Please try asking about 'list plant', 'become sitter', 'pricing', 'safety', 'care details', 'payment', 'cancelation', 'reviews', or 'contact support'."
}


@chat.route('/chat', methods=['GET'])
def chat_widget():
    return render_template('chat.html')

@chat.route('/api/chat', methods=['POST'])
def chat_api():
    user_message = request.json.get('message', '').strip().lower()
    response = FAQ_RESPONSES.get(user_message, FAQ_RESPONSES["default"])
    return jsonify({"response": response})