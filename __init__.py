 #####################################################################
#
#   JellyFin notifier
#       Announces new media added to Jellyfin
#
#
######################################################################
import json

from aiohttp.web import Request
from opsdroid.skill import Skill
from opsdroid.matchers import match_webhook

from opsdroid.events import Message, Reaction, Image, Video, RoomDescription

import requests

class JellyfinNotifier(Skill):
    def __init__(self, *args, **kwargs):
        super(JellyfinNotifier, self).__init__(*args, **kwargs)

    ##################################################################
    #
    #   1. Stream monitoring
    #       Monitors stream
    #
    ##################################################################
    @match_webhook('item_added')
    async def itemaddedwebhookskill(self, event: Request):
        # Capture the post data
        data = await event.text()
        data = json.loads(data)

        msg = f'<a href="{data["metadata"]["link"]}">{data["title"]}</a>'
        msg += f' now available on <a href="{self.config.get("jellyfin_url")}">Jellyfin</a>'
        if len(data['metadata']) > 1:
            data['metadata'].pop('link')
            links = ' '.join([f'<a href="{data["metadata"][key]}">{key}</a>' for key in data['metadata']])
            msg += f' ({links})'

        await self.opsdroid.send(
            Message(
                text=msg,
                target=self.config.get('room_notify')
            )
        )
