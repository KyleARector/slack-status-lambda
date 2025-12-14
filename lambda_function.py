import os
import json
import urllib.request
import urllib.error
import html

def update_slack_status(status, emoji):
  tokens = [val for key, val in os.environ.items() if "slack_token" in key]
  if not tokens:
    return
  url = "https://slack.com/api/users.profile.set"
  for token in tokens:
    profile = {
      "profile": {
        "status_text": status,
        "status_emoji": emoji,
        "status_expiration": 0
      }
    }
    data = json.dumps(profile).encode("utf-8")
    headers = {
      "Content-Type": "application/json;charset=utf-8",
      "Authorization": f"Bearer {token}"
    }
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
      with urllib.request.urlopen(req) as resp:
        body = resp.read().decode("utf-8")
        resp_json = json.loads(body)
        if not resp_json.get("ok"):
          raise Exception(f"Slack API error: {body}")
    except urllib.error.HTTPError as e:
      raise

def lambda_handler(event, context):
  status_options_str = ""
  if os.environ.get("status_options") is not None:
    status_options_str = os.environ["status_options"]
  else:
    f = open("status_options.json", "r")
    status_options_str = f.read()
    f.close()

  status_options = json.loads(status_options_str)

  # Normalize incoming event shapes to extract `status` or `index`.
  data = None
  if isinstance(event, dict):
    if "data" in event and isinstance(event["data"], dict):
      data = event["data"]
    elif "body" in event:
      try:
        data = json.loads(event["body"]) if isinstance(event["body"], str) else event["body"]
      except Exception:
        data = None
    elif "status" in event:
      data = {"status": event["status"]}
    elif "queryStringParameters" in event and event["queryStringParameters"]:
      q = event["queryStringParameters"]
      if "status" in q:
        data = {"status": q["status"]}

  if not data:
    raise KeyError("Must provide 'status' or 'index' in event. Supported shapes: {'data':{'status'|'index':...}}, {'status':...}, API GW with 'body' or 'queryStringParameters'}")

  # Resolve requested status from explicit name or numeric index
  requested = None
  if "index" in data:
    try:
      idx = int(data["index"])
    except Exception:
      raise KeyError("'index' must be an integer")
    keys = list(status_options.keys())
    n = len(keys)
    if 0 <= idx < n:
      requested = keys[idx]
    elif 1 <= idx <= n:
      requested = keys[idx - 1]
    else:
      raise IndexError(f"index out of range (got {idx}, valid 0..{n-1} or 1..{n})")
  elif "status" in data:
    requested = data["status"]
  else:
    raise KeyError("Must provide either 'status' or 'index' in event data")

  if requested in status_options or requested == "Clear":
    status = ""
    emoji = ""
    if requested != "Clear":
      status = requested
      emoji = status_options[status]
    update_slack_status(status, emoji)
  else:
    raise KeyError("The requested status is not in the list of statuses")


if __name__ == "__main__":
  print("This module is intended to be used as AWS Lambda. Call lambda_handler(event, context) with a valid event.")
