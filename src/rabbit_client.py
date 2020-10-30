import pika
import pickle


class RabbitMQReceiver:
    EXCHANGE_NAME = "ezwork_exchange"
    QUEUE_NAME = "tasks_receive"
    ROUTING_KEY = "new_task"

    def __init__(self, rabbitmq_params):
        self.RMQPARAMS = rabbitmq_params
        self.channel = None
        self.connection = None

    def connect(self):
        credentials = pika.PlainCredentials(self.RMQPARAMS.user, self.RMQPARAMS.password)
        parameters = pika.ConnectionParameters(
            self.RMQPARAMS.host,
            self.RMQPARAMS.port,
            self.RMQPARAMS.virtual_host,
            credentials,
            client_properties={'connection_name': 'rabbitmq-main-listener'}
        )

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=self.EXCHANGE_NAME,
                                      exchange_type='direct',
                                      passive=False,
                                      durable=True)

        self.channel.queue_declare(self.QUEUE_NAME, durable=True)
        self.channel.queue_bind(exchange=self.EXCHANGE_NAME,
                                queue=self.QUEUE_NAME,
                                routing_key=self.ROUTING_KEY)

    def get(self):
        try:
            result = None
            method_frame, header_frame, body = self.channel.basic_get(queue=self.QUEUE_NAME)
            if method_frame:
                data = pickle.loads(body)

                result = {
                    'data': data,
                    'method_frame': method_frame
                }

            return result
        except Exception:
            self.connect()

            return None
