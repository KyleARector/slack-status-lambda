import os
import slack

STATUS_OPTIONS = [
  ("", ""),
  ("Walking", ":walking:")
]

def lambda_handler(event, context):
  pos = 3
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
