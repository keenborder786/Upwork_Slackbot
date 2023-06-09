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


- `/generate`: Gives users recent job posting for the title given.

![Generate-Image](https://github.com/keenborder786/Upwork_Slackbot/blob/feat_interactivity/assets/GetCommand.png)

- `/Generate-Events`: Gives user an input prompt which allows them to write the job title and frequency at what they would like to get notify about the job while starting the continuous notifier

![Generate-Events-Image](https://github.com/keenborder786/Upwork_Slackbot/blob/docs_updating/assets/Modal_Image.png)

- `/stop`: Stop the the continuous notifier by `/Generate-Events`


