**********************
Mattermost Log Handler
**********************

Python log Handler that posts to a Mattermost channel. Post to
Mattermost using `Incoming
Webhooks <https://docs.mattermost.com/developer/webhooks-incoming.html>`__.
Inspired by https://github.com/mathiasose/slacker\_log\_handler and
others slack logs

Mattermost Log Handler use asyncio to generate requests non-blocking.

*exc\_info* is sent as a attachments

Mattermost don't support *icon\_emoji* as slack, maybe change icon\_url
to icon with differents levels of warnings, using /static/emoji as url
