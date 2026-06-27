import urllib.request, urllib.error, json

headers = {
    "Authorization": "Bearer rnd_RlzMGBHkr9X75xplhmy78IQw5mJL",
    "Content-Type": "application/json"
}

query = """
{
  deployments(input: { serviceId: "2e285e05-e61a-4402-aee8-d5f259a8e51a" }) {
    edges {
      node {
        id
        status
        createdAt
      }
    }
  }
}
"""

payload = json.dumps({"query": query}).encode()
req = urllib.request.Request(
    "https://backboard.railway.com/graphql/v2",
    data=payload,
    headers=headers,
    method="POST"
)
try:
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
        print(json.dumps(data, indent=2))
except urllib.error.HTTPError as e:
    print("Error:", e.code, e.read().decode())
