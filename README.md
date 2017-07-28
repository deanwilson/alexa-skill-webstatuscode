# Web Status Code Alexa Skill

Look up HTTP status codes using Alexa.

This project uses the [Serverless framework](https://serverless.com) and is
written in python 2(.7).

The name of this skill is technically a little incorrect, these are HTTP status
codes, not web ones, but I didn't want to invoke it with `h t t p status codes`

## Development docs

This is my first experiment with the Serverless framework so I'm leaving
slightly more in-depth documentation than you'd normally need.

### Create the serverless skeleton

This creates the basic config file and a stub python handler

    serverless create --template aws-python --path alexa-skill-webstatuscode

In my case I make this a git repo and add an empty, initial, commit.

### Edit the config file

    vi serverless.yml

Here is my [config file](/serverless.yml) for this project.

### Deploy the app to AWS

I use a dedicated set of credentials for this but you don't have to.

    AWS_PROFILE=admin serverless deploy -v

### View the logs

It'll break and you'll want to know why.

    AWS_PROFILE=admin serverless logs -f WebStatusCode

### Add the Alexa skill

These steps are all manual and done via the web console. I've added some text
files under `alexa/` to show examples of the intents and utterances I use.

### Author

[Dean Wilson](https://www.unixdaemon.net)

### License

 * GPLv2
