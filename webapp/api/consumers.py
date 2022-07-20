import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class ScanConsumer(AsyncWebsocketConsumer):
	async def connect(self):

		await self.channel_layer.group_add(
			"api",
			self.channel_name
		)
		await self.accept()

	async def disconnect(self, code):
		await self.channel_layer.group_discard(
		    "api",
		    self.channel_name
        )

	async def send_scan(self, scan):
		await self.send(text_data=json.dumps(
			{
				"id" : scan["id"],
				"mode" : scan["mode"],
				"login" : scan["login"],
				"validity" : scan["validity"],
				"event" : scan["event"],
			})
		)

