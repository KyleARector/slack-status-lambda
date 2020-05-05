import os
import slack

STATUS_OPTIONS = [
  ("", ""),
  ("Walking", ":walking:"),
  ("Eating", ":knife_fork_plate:"),
  ("On a video call", ":movie_camera:"),
  ("Walking the dog", ":dog2:"),
  ("In a meeting", ":busts_in_silhouette:"),
  ("Learning, but available", ":computer:"),
  ("Please do not disturb", ":octagonal_sign:"),
  ("On vacation", ":palm_tree:"),
  ("Commuting", ":car:")
]

def lambda_handler(event, context):
  if "status" in event["data"]:
    if event["data"]["status"] in dict(STATUS_OPTIONS):
      status = event["status"]
      clients = [slack.WebClient(val) for key, val in os.environ.items() if "slack_token" in key]
      for client in clients:
        client.users_profile_set(
          profile={
              "status_text": status,
              "status_emoji": dict(STATUS_OPTIONS)[status]
            }
        )
    else:
      raise KeyError("The requested status is not in the list of statuses")
  elif "index" in event["data"]:
    pos = event["data"]["index"]
    if 0 <= pos < len(STATUS_OPTIONS):
      clients = [slack.WebClient(val) for key, val in os.environ.items() if "slack_token" in key]
      for client in clients:
        client.users_profile_set(
          profile={
              "status_text": STATUS_OPTIONS[pos][0],
              "status_emoji": STATUS_OPTIONS[pos][1]
            }
        )
    else:
      raise IndexError("The requested status index is out of range.")
  else:
    raise BaseException("Must provide 'status' or 'index' argument in event")


if __name__ == "__main__":
  lambda_handler(None, None)
