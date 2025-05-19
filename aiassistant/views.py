import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import re

from django.core.exceptions import ObjectDoesNotExist

# Configure logging
logger = logging.getLogger(__name__)

# Enhanced symptom rules remain the same
SYMPTOM_RULES = {
    "chest pain": {"specialty": "Cardiology", "urgency": "Seek immediate care"},
    "shortness of breath": {"specialty": "Pulmonologist", "urgency": "Seek care today"},
    "headache": {"specialty": "Neurology", "urgency": "Schedule within a week"},
    "fever": {"specialty": "General Practitioner", "urgency": "Seek care if persistent"},
    "sore throat": {"specialty": "ENT", "urgency": "Schedule within a few days"},
    "abdominal pain": {"specialty": "Gastroenterologist", "urgency": "Seek care if severe"},
    "dizziness": {"specialty": "Internal Medicine", "urgency": "Schedule soon"},
    "skin rash": {"specialty": "Dermatology", "urgency": "Schedule within a week"},
    "joint pain": {"specialty": "Orthopedics", "urgency": "Schedule within a week"},
    "eye pain": {"specialty": "Ophthalmology", "urgency": "Seek care today"},
    "pregnancy": {"specialty": "Obstetrics & Gynecology", "urgency": "Schedule soon"},
    "flu": {"specialty": "General Practitioner", "urgency": "Seek care within 2 days"},
    "influenza": {"specialty": "General Practitioner", "urgency": "Seek care within 2 days"},
    "cough": {"specialty": "General Practitioner", "urgency": "Schedule within a week"},
    "cold": {"specialty": "General Practitioner", "urgency": "Schedule within a week"},
    "painful throat": {"specialty": "ENT", "urgency": "Schedule within a few days"},
    "throat pain": {"specialty": "ENT", "urgency": "Schedule within a few days"},
    "scratchy throat": {"specialty": "ENT", "urgency": "Schedule within a week"},
    "throat hurts": {"specialty": "ENT", "urgency": "Schedule within a few days"},
    "throat discomfort": {"specialty": "ENT", "urgency": "Schedule within a week"},
    "difficulty swallowing": {"specialty": "ENT", "urgency": "Schedule soon"},
    "hoarse voice": {"specialty": "ENT", "urgency": "Schedule within a week"},
}

SPECIALTY_DESCRIPTIONS = {
    "Pediatrics & Newborn": "Specializes in the health and medical care of infants, children, and adolescents up to age 18.",
    "Internal Medicine": "Focuses on adult medicine and the prevention, diagnosis, and treatment of complex illnesses.",
    "Obstetrics & Gynecology": "Provides care for women's reproductive health, pregnancy, childbirth, and postpartum care.",
    "Dentistry": "Diagnoses and treats conditions of the teeth, gums, and oral cavity including preventive care.",
    "Cardiology": "Specializes in heart and cardiovascular system disorders, including heart disease and hypertension.",
    "Orthopedics": "Treats musculoskeletal system issues including bones, joints, ligaments, tendons, and muscles.",
    "ENT (Ear, Nose & Throat)": "Manages conditions of the ears, nose, throat, head, and neck regions.",
    "General Surgery": "Performs surgical procedures for a wide range of conditions affecting different body parts.",
    "Neurology": "Diagnoses and treats disorders of the nervous system including brain and spinal cord conditions.",
    "Dermatology": "Specializes in skin, hair, and nail conditions including acne, eczema, and skin cancer.",
    "Ophthalmology": "Focuses on eye and vision care including medical and surgical treatments.",
    "Oncology": "Provides cancer care including diagnosis, chemotherapy, and management of malignant diseases."
}


@csrf_exempt
def chatbot_handler(request):
    """Handle all chatbot interactions with comprehensive error handling and debugging"""
    try:
        logger.info("Chatbot endpoint accessed - Method: %s", request.method)
        logger.debug(f"User: {request.user}, Authenticated: {request.user.is_authenticated}")

        # Enhanced debug logging
        logger.debug("Headers: %s", dict(request.headers))
        body_content = request.body.decode('utf-8') if request.body else 'Empty body'
        logger.debug("Body content: %s", body_content)
        logger.debug("Request META: %s", {k: v for k, v in request.META.items() if k.startswith('HTTP_')})

        if request.method != "POST":
            logger.warning("Invalid method %s received", request.method)
            return JsonResponse({
                "error": "Only POST method allowed",
                "status": "error"
            }, status=405, safe=False)

        # Parse JSON data with explicit error handling
        try:
            data = json.loads(request.body)
            logger.debug("Parsed request data: %s", data)
        except json.JSONDecodeError as e:
            logger.error("JSON decode error: %s", str(e))
            return JsonResponse({
                "error": "Invalid JSON format",
                "status": "error",
                "details": str(e)
            }, status=400, safe=False)

        # Extract parameters with defaults and log them
        message = data.get("message", "").lower().strip()
        action = data.get("action", "")
        user_id = data.get("user_id")

        logger.info("Processing request - Action: '%s', Message: '%s', User: %s",
                    action, message, user_id)

        # Route to appropriate handler with better logging
        response = None

        if action == "symptoms":
            logger.debug("Routing to symptoms handler")
            response = handle_symptoms(message, user_id)
        elif action == "book":
            logger.debug("Routing to booking handler")
            response = handle_booking(message, user_id, request)
        elif action == "specialties":
            logger.debug("Routing to specialties handler")
            response = handle_specialties(message)
        else:
            # Enhanced natural language query handling
            logger.debug("Processing natural language query")
            if any(greet in message for greet in ["hi", "hello", "hey"]):
                response = handle_greeting()
            elif any(key in message for key in SYMPTOM_RULES):
                response = handle_symptoms(message, user_id)
            elif "book" in message or "appointment" in message or "tomorrow" in message or "today" in message:
                response = handle_booking(message, user_id, request)
            elif any(term in message for term in ["special", "type", "kind", "doctor", "medical"]):
                response = handle_specialties(message)
            else:
                response = handle_unknown_query(message)

        # Validate response structure
        if not isinstance(response, dict):
            logger.error("Invalid response type: %s", type(response))
            response = {
                "messages": ["I encountered an internal error. Please try again."],
                "status": "error"
            }

        # Ensure messages array exists and is properly formatted
        if "messages" not in response:
            logger.warning("Response missing messages field")
            response["messages"] = ["I didn't get a proper response. Please try again."]

        # Set default status if missing
        response.setdefault("status", "success")

        logger.debug("Final response: %s", response)
        return JsonResponse(response, safe=False)

    except Exception as e:
        # Catch-all error handler
        logger.error("Unexpected error in chatbot_handler: %s", str(e), exc_info=True)
        return JsonResponse({
            "messages": ["I'm experiencing technical difficulties. Please try again later."],
            "status": "error",
            "system_error": str(e)
        }, status=500, safe=False)


# Supporting handler functions
def handle_greeting():
    """Handle greeting messages"""
    logger.debug("Handling greeting")
    return {
        "messages": [
            "Hello! I'm Doctorak Assistant. How can I help you today?",
            "You can:",
            "- Describe symptoms for medical advice",
            "- Ask to book an appointment",
            "- Inquire about medical specialties"
        ],
        "actions": [
            {"text": "Check Symptoms", "action": "symptoms"},
            {"text": "Book Appointment", "action": "book"},
            {"text": "View Specialties", "action": "specialties"}
        ]
    }


def handle_unknown_query(message):
    """Handle unrecognized queries"""
    logger.info("Unrecognized query: '%s'", message)
    return {
        "messages": [
            "I'm not sure I understand. Could you try:",
            "- Describing your symptoms",
            "- Asking to book an appointment",
            "- Inquiring about medical specialties"
        ],
        "actions": [
            {"text": "I have symptoms", "action": "symptoms"},
            {"text": "I want to book", "action": "book"},
            {"text": "Show specialties", "action": "specialties"}
        ]
    }


def handle_symptoms(message, user_id=None):
    """Handle symptom analysis with improved keyword matching"""
    try:
        logger.debug(f"Handling symptoms: '{message}'")
        found_keywords = []
        response = {"messages": [], "actions": [], "status": "success"}

        # Clean and normalize the input message
        message = message.lower().strip()
        logger.debug(f"Normalized message: '{message}'")

        # Sort keywords by length and specificity for better matching
        sorted_keywords = sorted(SYMPTOM_RULES.keys(), key=lambda x: (-len(x), x))
        logger.debug(f"Checking against {len(sorted_keywords)} keywords")

        # First pass: try to find exact matches
        for keyword in sorted_keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', message):
                info = SYMPTOM_RULES[keyword]
                found_keywords.append(keyword)
                logger.debug(f"Found exact match for keyword: '{keyword}'")

                response["messages"].append(
                    f"🔍 Based on '{keyword}': See {info['specialty']}. Urgency: {info['urgency']}"
                )
                response["actions"].append({
                    "text": f"📅 Book {info['specialty']}",
                    "url": reverse('doctor_list') + f"?specialty={info['specialty']}"
                })
                break  # Stop after first exact match

        # Second pass: if no exact matches, try partial matches
        if not found_keywords:
            logger.debug("No exact matches found, trying partial matches")
            for keyword in sorted_keywords:
                if keyword in message:
                    info = SYMPTOM_RULES[keyword]
                    found_keywords.append(keyword)
                    logger.debug(f"Found partial match for keyword: '{keyword}'")

                    response["messages"].append(
                        f"🔍 Based on '{keyword}': See {info['specialty']}. Urgency: {info['urgency']}"
                    )
                    response["actions"].append({
                        "text": f"📅 Book {info['specialty']}",
                        "url": reverse('doctor_list') + f"?specialty={info['specialty']}"
                    })
                    break  # Stop after first partial match

        # If still no matches, suggest general practitioner
        if not found_keywords:
            logger.debug("No symptom matches found")
            response["messages"].append(
                f"🤔 I didn't recognize specific symptoms in: '{message}'. You might want to consult a General Practitioner."
            )
            response["actions"].append({
                "text": "👨‍⚕️ Consult General Practitioner",
                "url": reverse('doctor_list') + "?specialty=General%20Practitioner"
            })

        logger.debug(f"Symptom response: {response}")
        return response

    except Exception as e:
        logger.error(f"Symptom analysis error: {str(e)}", exc_info=True)
        return {
            "messages": ["⚠️ Symptom analysis failed. Please try again."],
            "status": "error"
        }


def handle_booking(message=None, user_id=None, request=None):
    """Handle appointment booking with improved date/time detection"""
    try:
        logger.debug(f"Handling booking: '{message}'")
        response = {"messages": [], "actions": [], "status": "success"}

        # Normalize message and fix common typos
        message = (message or "").lower().strip()
        message = message.replace("tommorow", "tomorrow")
        logger.debug(f"Normalized booking message: '{message}'")

        # Check if the message is empty or None
        if not message:
            logger.debug("Empty booking message")
            response["messages"].extend([
                "📅 To book an appointment:",
                "1. Tell me when (e.g., 'tomorrow at 2 PM' or 'Friday 3 PM')",
                "2. I'll show available doctors",
                "3. Select your preferred doctor"
            ])
            response["actions"].append({
                "text": "👨‍⚕️ Browse All Doctors",
                "url": reverse('doctor_list')
            })
            return response

        # Improved date pattern with typo tolerance
        date_pattern = r'(today|tomorrow|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}(?:st|nd|rd|th)?(?:\s+of)?\s+(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)(?:\s+\d{2,4})?)'
        date_match = re.search(date_pattern, message, re.IGNORECASE)

        # Improved time pattern to match various formats
        time_pattern = r'(\d{1,2}(?::\d{2})?\s*(?:am|pm)|(?:at|around|by)\s+\d{1,2}(?::\d{2})?\s*(?:am|pm)?)'
        time_match = re.search(time_pattern, message, re.IGNORECASE)

        # Extract the time portion if it's in the format "at X" or "by X"
        if time_match:
            time_text = time_match.group(1)
            # If the time includes "at" or "by", extract just the time part
            if time_text.startswith(("at ", "around ", "by ")):
                time_parts = time_text.split()
                if len(time_parts) >= 2:
                    time_text = " ".join(time_parts[1:])  # Skip the "at"/"by" part
            logger.debug(f"Extracted time: '{time_text}'")
        else:
            time_text = "any time"
            logger.debug("No specific time mentioned")

        # Process date and time information
        if date_match:
            date = date_match.group(1)
            logger.debug(f"Detected date: '{date}', time: '{time_text}'")

            response["messages"].extend([
                f"⏰ I'll find available doctors for {date} at {time_text}",
                "Choose a specialty:"
            ])

            # Get unique specialties from symptom rules
            specialties = sorted(set(info['specialty'] for info in SYMPTOM_RULES.values()))
            logger.debug(f"Providing {len(specialties)} specialty options")

            # Create actions for each specialty
            response["actions"] = [
                {
                    "text": spec,
                    "url": reverse('doctor_list') + f"?date={date}&time={time_text}&specialty={spec}"
                } for spec in specialties[:8]  # Limit to 8 options to avoid overwhelming the UI
            ]

            # Add "More Specialties" option if needed
            if len(specialties) > 8:
                response["actions"].append({
                    "text": "More Specialties",
                    "url": reverse('doctor_list') + f"?date={date}&time={time_text}"
                })

            # Add fallback if no time specified
            if not time_match:
                response["messages"].append("⌚ You can specify a time like '2 PM' for better results")

        else:
            # Check if the message contains time but no date (like "2 PM" without specifying day)
            if time_match and not date_match:
                logger.debug(f"Time mentioned ({time_text}) but no date detected")
                response["messages"].extend([
                    f"⌚ I see you'd like an appointment at {time_text}.",
                    "When would you like this appointment? (e.g., today, tomorrow, or a specific date)"
                ])
                response["actions"].append({
                    "text": "👨‍⚕️ Browse All Doctors",
                    "url": reverse('doctor_list')
                })
            else:
                logger.debug("No date detected in booking message")
                response["messages"].extend([
                    "📅 To book an appointment:",
                    "1. Tell me when (e.g., 'tomorrow at 2 PM' or 'Friday 3 PM')",
                    "2. I'll show available doctors",
                    "3. Select your preferred doctor"
                ])
                response["actions"].append({
                    "text": "👨‍⚕️ Browse All Doctors",
                    "url": reverse('doctor_list')
                })

        logger.debug(f"Booking response: {response}")
        return response

    except Exception as e:
        logger.error(f"Booking error: {str(e)}", exc_info=True)
        return {
            "messages": ["⚠️ Booking system unavailable. Try again later."],
            "status": "error"
        }


def handle_specialties(message=None):
    """Provide information about medical specialties"""
    try:
        logger.debug("Handling specialties request")

        # Filter and sort specialties by relevance
        specialties_list = [
            f"• {spec}: {desc[:100]}..." if len(desc) > 100 else f"• {spec}: {desc}"
            for spec, desc in SPECIALTY_DESCRIPTIONS.items()
        ]

        response = {
            "messages": [
                "🏥 Available Medical Specialties:",
                *specialties_list[:6],  # Show only first 6 to avoid overwhelming the user
                "ℹ️ Select a specialty to see available doctors"
            ],
            "actions": [
                {
                    "text": spec.split(":")[0].strip("• "),
                    "url": reverse('doctor_list') + f"?specialty={spec.split(':')[0].strip('• ')}"
                } for spec in specialties_list[:6]
            ]
        }

        # Add "See All Specialties" as the last action
        response["actions"].append({
            "text": "👨‍⚕️ See All Specialties",
            "url": reverse('doctor_list')
        })

        logger.debug(f"Specialties response: {response}")
        return response

    except Exception as e:
        logger.error("Specialties handler failed: %s", str(e), exc_info=True)
        return {
            "messages": ["⚠️ Couldn't retrieve specialties. Try again later."],
            "status": "error"
        }


def handle_general(message):
    """Handle general conversation with fallbacks"""
    try:
        logger.debug(f"Handling general message: '{message}'")
        greetings = ["hi", "hello", "hey"]
        if any(greet in message for greet in greetings):
            return {
                "messages": [
                    "Hello! I'm Doctorak Assistant. How can I help you today?",
                    "You can describe your symptoms, ask about specialties, or book an appointment."
                ],
                "status": "success"
            }

        return {
            "messages": [
                "I'm not sure I understand. Could you rephrase that?",
                "I can help with: symptom checking, booking appointments, or explaining medical specialties."
            ],
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error in handle_general: {str(e)}", exc_info=True)
        return {
            "messages": ["I'm having trouble understanding. Please try again."],
            "status": "error"
        }
