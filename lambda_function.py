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

  print(status_options)

  if "status" in event["data"]:
    if event["data"]["status"] in dict(status_options) or event["data"]["status"] == "Clear":
      status = ""
      emoji = ""
      if event["data"]["status"] != "Clear":
        status = event["data"]["status"]
        emoji = dict(status_options)[status]
      update_slack_status(status, emoji)
    else:
      raise KeyError("The requested status is not in the list of statuses")
  elif "index" in event["data"]:
    pos = event["data"]["index"]
    if 0 <= pos < len(status_options):
      update_slack_status(status_options[pos][0], status_options[pos][1])
    else:
      raise IndexError("The requested status index is out of range.")
  else:
    raise BaseException("Must provide 'status' or 'index' argument in event")


if __name__ == "__main__":
  lambda_handler(None, None)
