import os
import slack

STATUS_OPTIONS = [
  ("", ""),
  ("Walking", ":walking:"),
  ("Eating", ":knife_fork_plate:"),
  ("On a video call", ":movie_camera:"),
  ("Available", ":white_check_mark:"),
  ("Learning, but available", ":computer:"),
  ("Please do not disturb", ":no_entry:"),
  ("Out for the day", ":rocket:"),
  ("In a meeting", ":busts_in_silhouette:"),
  ("Walking the dog", ":dog2:"),
  ("Making tea", ":tea:"),
  ("Commuting", ":car:"),
  ("On vacation", ":palm_tree:"),
  ("Meditating", ":man_in_lotus_position:"),
  ("Doing yoga", ":man_in_lotus_position:"),
  ("Hardware hacking", ":robot_face:"),
  ("Working on Hacktoberfest", ":jack_o_lantern:"),
  ("Working on Advent of Code", ":snowflake:"),
]

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
  if "status" in event["data"]:
    if event["data"]["status"] in dict(STATUS_OPTIONS) or event["data"]["status"] == "Clear":
      status = ""
      emoji = ""
      if event["data"]["status"] != "Clear":
        status = event["data"]["status"]
        emoji = dict(STATUS_OPTIONS)[status]
      update_slack_status(status, emoji)
    else:
      raise KeyError("The requested status is not in the list of statuses")
  elif "index" in event["data"]:
    pos = event["data"]["index"]
    if 0 <= pos < len(STATUS_OPTIONS):
      update_slack_status(STATUS_OPTIONS[pos][0], STATUS_OPTIONS[pos][1])
    else:
      raise IndexError("The requested status index is out of range.")
  else:
    raise BaseException("Must provide 'status' or 'index' argument in event")


if __name__ == "__main__":
  lambda_handler(None, None)
