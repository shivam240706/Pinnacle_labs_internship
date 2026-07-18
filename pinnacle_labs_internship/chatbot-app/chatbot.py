"""
chatbot.py
-----------
Core response engine for "Masha".

Approach: rule-based keyword matching.
Why rule-based instead of an ML model?
- Fully deterministic and explainable to a beginner
- No model download / training required -> zero setup risk
- Easy to extend: add a keyword, add a reply
"""

import random
import re

# Each intent maps to: trigger keywords + a list of possible replies
INTENTS = {
    "greeting": {
        "keywords": ["hi", "hello", "hey", "good morning", "good evening"],
        "replies": [
            "Hello! 👋 I'm Masha. How can I help you today?",
            "Hi there! What can I do for you today?",
        ],
    },
    # Complaint and return/refund are checked before product_info/order_status
    # on purpose: a message like "this product arrived broken" should be
    # treated as an urgent complaint, not a generic product question.
    "complaint": {
        "keywords": ["broken", "damaged", "bad", "angry", "disappointed", "terrible", "worst"],
        "replies": [
            "I'm really sorry to hear that. That's not the experience we want "
            "for you — I'm escalating this to a human support agent right away.",
        ],
    },
    "return_refund": {
        "keywords": ["return", "refund", "cancel", "exchange", "money back"],
        "replies": [
            "No problem. Our return policy allows returns within 30 days of "
            "delivery. Would you like me to start a return request?",
        ],
    },
    "order_status": {
        "keywords": ["order", "track", "delivery", "shipment", "shipping", "package"],
        "replies": [
            "I can help with that! Please share your Order ID (e.g. #PL12345) "
            "and I'll look up the status.",
        ],
    },
    "product_info": {
        "keywords": ["price", "product", "available", "stock", "cost", "catalog"],
        "replies": [
            "You can browse our full catalog and live pricing on the "
            "Products page. Is there a specific item you're looking for?",
        ],
    },
    "hours_contact": {
        "keywords": ["hours", "open", "contact", "phone", "email", "reach"],
        "replies": [
            "We're open Mon-Sat, 9 AM - 7 PM. You can reach us at "
            "support@pinnaclelabs.example or +1-555-0100.",
        ],
    },
    "human_handoff": {
        "keywords": ["human", "agent", "representative", "person", "someone"],
        "replies": [
            "Sure thing — connecting you with a human support agent now. "
            "Please hold for a moment.",
        ],
    },
    "thanks": {
        "keywords": ["thanks", "thank you", "appreciate", "thx"],
        "replies": [
            "You're very welcome! 😊 Anything else I can help with?",
        ],
    },
    "goodbye": {
        "keywords": ["bye", "goodbye", "exit", "quit", "see you"],
        "replies": [
            "Thanks for chatting with us — have a great day! 👋",
        ],
    },
}

FALLBACK_REPLIES = [
    "I didn't quite catch that. Could you rephrase, or pick one of the quick "
    "options below?",
]

# Quick-reply suggestions shown on the fallback (used by the Streamlit UI)
QUICK_REPLIES = [
    "Track my order",
    "Return a product",
    "Store hours",
    "Talk to a human",
]


def get_response(user_message: str) -> dict:
    """
    Determine the bot's reply to a user message.

    Args:
        user_message: Raw text typed by the user.

    Returns:
        {
            "intent": matched intent name, or "fallback",
            "reply": the bot's text reply,
        }
    """
    if not user_message or not user_message.strip():
        return {"intent": "fallback", "reply": random.choice(FALLBACK_REPLIES)}

    text = user_message.lower()

    for intent_name, intent_data in INTENTS.items():
        for keyword in intent_data["keywords"]:
            # \b = word boundary, so "hi" matches "hi" but not "this"
            pattern = r"\b" + re.escape(keyword) + r"\b"
            if re.search(pattern, text):
                return {
                    "intent": intent_name,
                    "reply": random.choice(intent_data["replies"]),
                }

    return {"intent": "fallback", "reply": random.choice(FALLBACK_REPLIES)}


if __name__ == "__main__":
    # Quick manual sanity check - run with: python chatbot.py
    test_messages = [
        "Hi there!",
        "Where is my order #PL12345?",
        "I want a refund for this item",
        "This product arrived broken and I'm furious",
        "What are your store hours?",
        "asdkjaskdj random gibberish",
        "thanks a lot!",
        "bye",
    ]
    for msg in test_messages:
        result = get_response(msg)
        print(f"User: {msg!r:45} -> Intent: {result['intent']:15} Reply: {result['reply']}")
