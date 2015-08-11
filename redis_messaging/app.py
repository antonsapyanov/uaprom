import redis
import threading
import sys


class PubSubApplication(object):
    def __init__(self, host, port):
        self.COMMANDS = {
            'sub': self.subscribe,
            'unsub': self.unsubscribe,
            'pub': self.publish,
            'quit': self.quit
        }

        self._server = redis.StrictRedis(host, port)
        self._pubsub = self._server.pubsub()

        self._already_created_thread = False
        self._username = None

    def run(self):
        self._username = input('Enter your username: ')
        while True:
            input_dict = self.parse_input(input())
            if input_dict['command'] not in self.COMMANDS:
                self.show_error('there is no such command; '
                                'use one from next: {}'.format(', '.join(self.COMMANDS.keys())))
            else:
                self.execute(input_dict['command'], input_dict['params'])

    def execute(self, command, params):
        return self.COMMANDS[command](params)

    def publish(self, params):
        params = params.split(' ', 1)
        if len(params) < 2:
            self.show_error('expected at least 2 parameters: channel and message; '
                            '{0} is given: {1}'.format(len(params), params))
            return
        channel = params[0]
        message = params[1]
        self._server.publish(channel, "{user}: {message}".format(user=self._username, message=message))

    def subscribe(self, channels):
        channels = channels.split(' ')
        if len(channels) == 0:
            self.show_error('expected at least 1 channel, nothing is given')
        self._pubsub.subscribe(channels)

        if not self._already_created_thread:
            messaging_thread = threading.Thread(target=self._notification_thread)
            messaging_thread.start()
            self._already_created_thread = True

    def _notification_thread(self):
        for message in self._pubsub.listen():
            channel = message['channel'].decode()
            data = message['data'].decode() if isinstance(message['data'], bytes) else message['data']
            print("({channel}) {data}".format(channel=channel,
                                              data=data))

    def unsubscribe(self, channels=None):
        if channels is not None:
            self._pubsub.unsubscribe(channels.split(' '))
        else:
            self._pubsub.unsubscribe()

    def quit(self, *args):
        self.unsubscribe()
        print('Bye, bye {user}'.format(user=self._username))
        sys.exit(0)

    @staticmethod
    def parse_input(input_string):
        input_list = input_string.split(' ', 1)
        input_dict = {
            'command': input_list[0],
            'params': input_list[1] if len(input_list) > 1 else ''
        }
        return input_dict

    @staticmethod
    def show_error(message):
        print('error: {}'.format(message))
