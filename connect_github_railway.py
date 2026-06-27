"""Connect Railway service to GitHub repo directly via GraphQL API"""
import urllib.request, urllib.error, json

# Railway public token (from railway CLI session)
TOKEN = "rnd_RlzMGBHkr9X75xplhmy78IQw5mJL"
SERVICE_ID = "2e285e05-e61a-4402-aee8-d5f259a8e51a"
PROJECT_ID = "062eb87c-d02c-4b4d-9fdd-a7388d9f6121"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Update service to use GitHub repo source with rootDir=backend
mutation = """
mutation {
  serviceUpdate(
    id: "%s"
    input: {
      source: {
        repo: "lokeshpatil2602/customer-churn-prediction-system"
        branch: "main"
      }
      rootDirectory: "backend"
      buildCommand: "pip install -r requirements.txt"
      startCommand: "gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120"
    }
  ) {
    id
    name
  }
}
""" % SERVICE_ID

payload = json.dumps({"query": mutation}).encode()
req = urllib.request.Request(
    "https://backboard.railway.com/graphql/v2",
    data=payload,
    headers=headers,
    method="POST"
)
try:
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
        print("Response:", json.dumps(data, indent=2))
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"HTTP {e.code}:", body)
