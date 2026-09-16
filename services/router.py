def classify_request(question):

    question = question.lower()

    if "inc" in question:
        return "incident_lookup"

    if "active p1" in question:
        return "active_incidents"

    if "vpn" in question:
        return "historical_search"

    return "general_query"
