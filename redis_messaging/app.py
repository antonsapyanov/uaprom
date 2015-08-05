import redis


class PubSubApplication(object):
    def __init__(self, host, port):
        self.COMMANDS = {
            'subscribe': self.subscribe,
            'publish': self.publish
        }

        self.server = redis.StrictRedis(host, port)

    def run(self):
        try:
            while True:
                input_dict = self.parse_input(input('> '))
                if input_dict['command'] not in self.COMMANDS:
                    self.show_error('there is no such command')
                else:
                    self.execute(input_dict['command'], input_dict['params'])
        except KeyboardInterrupt:
            return

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
        self.server.publish(channel, message)

    def subscribe(self, channels):
        channels = channels.split(' ')
        if len(channels) == 0:
            self.show_error('expected at least 1 channel, nothing is given')
        pubsub = self.server.pubsub()
        pubsub.subscribe(channels)
        try:
            for message in pubsub.listen():
                print("{channel}: {message}".format(channel=message['channel'].decode(),
                                                    message=message['data']))
        except KeyboardInterrupt:
            return

    @staticmethod
    def parse_input(input_string):
        input_list = input_string.split(' ', 1)
        input_dict = {
            'command': input_list[0],
            'params': input_list[1]
        }
        return input_dict

    @staticmethod
    def show_error(message):
        print('error: {}'.format(message))
