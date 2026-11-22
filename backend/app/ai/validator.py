import json
from typing import Dict, Any, Tuple
from app.schemas.ai import AIInsightOutputSchema

def validate_ai_output(raw_response_text: str) -> Tuple[bool, Dict[str, Any], str]:
    """
    Validates that LLM output is valid JSON and strictly conforms to AIInsightOutputSchema.
    Returns (is_valid, parsed_dict, error_message).
    """
    text = raw_response_text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        return False, {}, f"JSON Decode Error: {str(e)}"

    try:
        validated = AIInsightOutputSchema.model_validate(data)
        return True, validated.model_dump(), ""
    except Exception as e:
        return False, {}, f"Schema Validation Error: {str(e)}"
