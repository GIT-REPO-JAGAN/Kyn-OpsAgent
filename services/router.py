import re

INCIDENT_PATTERN = re.compile(
    r"\bINC\d+\b",
    re.IGNORECASE,
)

def classify_request(question):

    text = question.lower()

    incident_match = INCIDENT_PATTERN.search(question)

    incident_number = None

    if incident_match:
        incident_number = incident_match.group(0)

    if any(
        phrase in text
        for phrase in [
            "close incident",
            "resolve incident",
            "update incident",
            "change priority",
            "assign incident",
        ]
    ):
        return {
            "intent": "servicenow_update",
            "incident_number": incident_number,
            "tool": "servicenow_write",
        }

    if any(
        phrase in text
        for phrase in [
            "active p1",
            "active incidents",
            "open incidents",
            "list incidents",
        ]
    ):
        return {
            "intent": "active_incidents",
            "incident_number": incident_number,
            "tool": "servicenow_read",
        }

    if any(
        phrase in text
        for phrase in [
            "similar",
            "related",
            "historical",
            "find incidents",
        ]
    ):
        return {
            "intent": "historical_search",
            "incident_number": incident_number,
            "tool": "knowledge_base",
        }

    if incident_number:
        return {
            "intent": "incident_lookup",
            "incident_number": incident_number,
            "tool": "knowledge_base",
        }

    return {
        "intent": "resolution_recommendation",
        "incident_number": None,
        "tool": "knowledge_base",
    }
