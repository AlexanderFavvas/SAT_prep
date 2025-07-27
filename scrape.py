import requests
import json
import time


METADATA_URL = "https://qbank-api.collegeboard.org/msreportingquestionbank-prod/questionbank/digital/get-questions"
QUESTION_URL = "https://qbank-api.collegeboard.org/msreportingquestionbank-prod/questionbank/digital/get-question"


HEADERS = {
    "Accept":       "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin":       "https://satsuitequestionbank.collegeboard.org",
    "Referer":      "https://satsuitequestionbank.collegeboard.org/",
    "User-Agent":   ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/136.0.0.0 Safari/537.36"),
}


meta_payload = {
    "asmtEventId": 99,
    "test":        2,
    "domain":     "H,P,Q,S",
}

session = requests.Session()
session.headers.update(HEADERS)


r_meta = session.post(METADATA_URL, json=meta_payload, timeout=5)
r_meta.raise_for_status()
metadata_list = r_meta.json()

print(f"Found {len(metadata_list)} question stubs.")


all_questions = []
for idx, stub in enumerate(metadata_list, start=1):
    external_id = stub.get("external_id")
    if not external_id:
        print(f"  → Skipping question stub {idx} because it is missing an external_id.")
        continue
        
    payload = {"external_id": external_id}
    try:
        r_q = session.post(QUESTION_URL, json=payload, timeout=5)
        r_q.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"  → Error fetching {external_id}: {e}")
        print(f"    Response status: {e.response.status_code}")
        print(f"    Response text: {e.response.text}")
        print("  → Getting a new session.")
        session = requests.Session()
        session.headers.update(HEADERS)
        continue
    except Exception as e:
        print(f"  → Error fetching {external_id}: {e}")
        print("  → Getting a new session.")
        session = requests.Session()
        session.headers.update(HEADERS)
        continue

    question_data = r_q.json()

    if "$fault" in question_data and question_data["$fault"] == "client":
        print(f"  → API Error for {external_id}: {question_data.get('message', 'No message')}")
        continue

    all_questions.append(question_data)

    print(f"[{idx}/{len(metadata_list)}] fetched question {external_id}")


    # be polite
    time.sleep(0.2)

# save
with open("all_questions.json", "w", encoding="utf-8") as f:
    json.dump(all_questions, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(all_questions)} full questions to all_questions.json")
