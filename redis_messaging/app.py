import redis
import threading
import sys


class PubSubApplication(object):
    def __init__(self, host, port):
        self.COMMANDS = {
            'subscribe': self.subscribe,
            'unsubscribe': self.unsubscribe,
            'publish': self.publish,
            'quit': self.quit
        }

        self.server = redis.StrictRedis(host, port)
        self.pubsub = self.server.pubsub()

        self.username = None

    def run(self):
        self.username = input('Enter your username: ')
        while True:
            input_dict = self.parse_input(input())
            if input_dict['command'] not in self.COMMANDS:
                self.show_error('there is no such command')
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
        self.server.publish(channel, "{user}: {message}".format(user=self.username, message=message))

    def subscribe(self, channels):
        channels = channels.split(' ')
        if len(channels) == 0:
            self.show_error('expected at least 1 channel, nothing is given')
        self.pubsub.subscribe(channels)

        messaging_thread = threading.Thread(target=self._notification_thread)
        messaging_thread.start()

    def _notification_thread(self):
        for message in self.pubsub.listen():
            print("({channel}) {message}".format(channel=message['channel'].decode(),
                                                message=message['data']))

    def unsubscribe(self, channels=None):
        if channels is not None:
            self.pubsub.unsubscribe(channels.split(' '))
        else:
            self.pubsub.unsubscribe()

    def quit(self, *args):
        self.unsubscribe()
        print('Bye, bye {user}'.format(user=self.username))
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
