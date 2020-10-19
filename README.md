# Slack Status Lambda 
An AWS Lambda function to update your slack status from a list of presets. The lambda uses only basic Slack emoji, not custom, so that it can be used in any new Slack workspace.

Additionally, the lambda may target multiple Slack workspaces to ensure that the status is synced between them. To enable this for additional workspaces, add the new workspace's bot token to an environment variable for the lambda on AWS, ensuring that `slack_token` is in the name of the variable. For example, for 2 different workspaces, the env variables may include `my_slack_token` and `your_slack_token`.

![Deploy Lambda](https://github.com/KyleARector/slack-status-lambda/workflows/Deploy%20Lambda/badge.svg)
