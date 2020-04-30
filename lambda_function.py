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
  pos = event["status"]
  if 0 <= pos < len(STATUS_OPTIONS):
    client = slack.WebClient(token=os.environ["slack_token"])
    client.users_profile_set(
      profile={
          "status_text": STATUS_OPTIONS[pos][0],
          "status_emoji": STATUS_OPTIONS[pos][1]
        }
    )
  else:
    raise IndexError("The requested status index is out of range.")


if __name__ == "__main__":
  lambda_handler(None, None)
