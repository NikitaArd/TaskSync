import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


from .ws_views import (
    task_shift,
    task_add,
    task_status_edit,
    task_delete,
    task_content_edit,
    column_add,
    column_delete,
    column_name_edit,
    chat_message,
)

class ProjectConsumer(WebsocketConsumer):
    def connect(self):
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.room_group_name = 'project_{}'.format(self.project_id)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        context = dict()

        if text_data_json['request_type'] == 'task_shift':     

            context = task_shift(text_data_json)


        elif text_data_json['request_type'] == 'task_add':

            context = task_add(text_data_json)


        elif text_data_json['request_type'] == 'task_status_edit':

            context = task_status_edit(text_data_json)

        
        elif text_data_json['request_type'] == 'task_delete':

            context = task_delete(text_data_json)


        elif text_data_json['request_type'] == 'task_content_edit':

            context = task_content_edit(text_data_json)

        
        elif text_data_json['request_type'] == 'column_add':

            context = column_add(text_data_json)


        elif text_data_json['request_type'] == 'column_delete':

            context = column_delete(text_data_json)


        elif text_data_json['request_type'] == 'column_name_edit':

            context = column_name_edit(text_data_json)


        elif text_data_json['request_type'] == 'chat_message':

            context = chat_message(text_data_json)

        context['type'] = 'context_response'


        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, context
        )

    # Response function

    def context_response(self, event):
        self.send(text_data=json.dumps(event))

