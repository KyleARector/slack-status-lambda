import os
import json
import slack

def update_slack_status(status, emoji):
  clients = [slack.WebClient(val) for key, val in os.environ.items() if "slack_token" in key]
  for client in clients:
    client.users_profile_set(
      profile={
          "status_text": status,
          "status_emoji": emoji,
          "status_expiration": 0
        }
    )

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
  lambda_handler(None, None)
