import pika


class Keeper():
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.51', port=32770))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='query')

    def basic_publish(self, **kwargs):
        try:
            if self.connection.is_closed:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.51', port=32770))
                self.channel = self.connection.channel()

            if self.channel.is_closed:
                self.channel = self.connection.channel()
            self.channel.basic_publish(**kwargs)
        except:
            self.basic_publish(**kwargs)


channel = Keeper()