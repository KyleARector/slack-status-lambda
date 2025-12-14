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

  if "status" in event["data"]:
    if event["data"]["status"] in status_options or event["data"]["status"] == "Clear":
      status = ""
      emoji = ""
      if event["data"]["status"] != "Clear":
        status = event["data"]["status"]
        emoji = status_options[status]
      update_slack_status(status, emoji)
    else:
      raise KeyError("The requested status is not in the list of statuses")
  else:
    raise BaseException("Must provide 'status' argument in event")


if __name__ == "__main__":
  print("This module is intended to be used as AWS Lambda. Call lambda_handler(event, context) with a valid event.")
