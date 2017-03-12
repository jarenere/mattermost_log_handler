import json
import requests
import asyncio
import functools
import traceback
from logging import Handler, CRITICAL, ERROR, WARNING, INFO, FATAL, DEBUG, NOTSET
import logging


DEFAULT_TIMEOUT = 10
ERROR_COLOR = 'danger'  # color name is built in to Mattermost API
WARNING_COLOR = 'warning'  # color name is built in to Mattermost API
INFO_COLOR = 'good'  # color name is built in to Mattermost API

COLORS = {
    CRITICAL: ERROR_COLOR,
    FATAL: ERROR_COLOR,
    ERROR: ERROR_COLOR,
    WARNING: WARNING_COLOR,
    INFO: INFO_COLOR,
    DEBUG: INFO_COLOR,
    NOTSET: INFO_COLOR,
}


class MattermostLogHandler(Handler):
    def __init__(self, webhook_url, username=':exclamation:  Python logger',
                 channel=None, icon_url=None, timeout=None, proxies={},
                 verify=True, format=None, asyncio_requests=False):
        Handler.__init__(self)
        self.webhook_url = webhook_url
        self.channel = channel
        self.username = username
        self.icon_url = icon_url
        self.session = requests.session()
        self.session.proxies = proxies
        self.session.verify = verify
        self.session.timeout = DEFAULT_TIMEOUT if timeout is None else timeout
        self.session.headers.update({'Content-Type': 'application/json'})
        if format is not None:
            self.formatter = logging.Formatter(format)
        self.asyncio_requests = asyncio_requests
        if self.asyncio_requests:
            self.loop = asyncio.get_event_loop()

    def _build_msg(self, record):
        if record.exc_info is None:
            return self.format(record)

        exc_info_tmp = record.exc_info
        record.exc_info = None
        msg = self.format(record)
        record.exc_info = exc_info_tmp
        return msg

    def _build_trace(self, record, fallback):
        if record.exc_info is None:
            return None

        trace = {
            'fallback': fallback,
            'color': COLORS.get(record.levelno, INFO_COLOR)
        }
        if record.exc_info:
            trace['text'] = '\n'.join(traceback.format_exception(*record.exc_info))
        return [trace]

    def emit(self, record):
        message = self._build_msg(record)
        attachments = self._build_trace(record, fallback=message)

        payload = {
            "text": message,
            "username": self.username,
        }
        if attachments is not None:
            payload['attachments'] = attachments

        if self.icon_url is not None:
            payload['icon_url'] = self.icon_url
        if self.channel is not None:
            payload['channel'] = self.channel
        if self.asyncio_requests:
            self.loop.run_in_executor(
                None,
                functools.partial(self.session.post,
                                  self.webhook_url,
                                  data=json.dumps(payload)))
        else:
            self.session.post(self.webhook_url, data=json.dumps(payload))
