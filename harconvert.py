import json

# Load HAR file (exported from Chrome DevTools)
with open("doc.har", "r", encoding="utf-8") as f:
    har_data = json.load(f)

entries = har_data["log"]["entries"]

structured_requests = []

for entry in entries:
    request = entry["request"]
    response = entry["response"]

    item = {
        "method": request["method"],
        "url": request["url"],
        "request_headers": {h["name"]: h["value"] for h in request.get("headers", [])},
        "request_body": request.get("postData", {}).get("text", None),
        "status": response["status"],
        "response_headers": {h["name"]: h["value"] for h in response.get("headers", [])},
        "response_body_size": response.get("content", {}).get("size", 0),
        "response_mime": response.get("content", {}).get("mimeType", ""),
        "response_body": response.get("content", {}).get("text", None)  # may be base64
    }

    structured_requests.append(item)

# Save to a new JSON file
with open("doc.json", "w", encoding="utf-8") as out:
    json.dump(structured_requests, out, indent=2)
