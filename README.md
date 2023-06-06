# Upwork SlackBot


## Parameters Requirements
In order to run the slack-bot you will need to set up the followig env variables:

- [SLACK_BOT_TOKEN](https://api.slack.com/authentication/oauth-v2)
- SLACK_APP_TOKEN: These are app-level token allowing your app to use platform features that apply to multiple (or all) installations. You need to generate then when you create your app.
- CHANNEL_ID: The channel where bot responds to.


## Run the Bot

```
docker-compose up
```

## Bot commands:


- `/generate`: Generate the jobs for the given query. Will ask for the time interval

![https://github.com/keenborder786/Upwork_Slackbot/blob/feat_interactivity/assets/GetCommand.png]


