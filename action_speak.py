import json
import pika
import pyttsx3

engine = pyttsx3.init()
input_exchange = 'action_speech'


def say_something(ch, method, properties, body):
    payload = json.loads(body)
    engine.say(payload['data'])
    engine.runAndWait()


def maragi_subscribe():
    parameters = pika.URLParameters('amqp://guest:guest@maragi-rabbit:5672/%2F')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare(exchange=input_exchange, exchange_type='fanout')
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=input_exchange, queue=queue_name)
    channel.basic_consume(say_something, queue=queue_name, no_ack=True)
    channel.start_consuming()


if __name__ == "__main__":
    while True:
        try:
            maragi_subscribe()
        except Exception as oops:
            print('ERROR:', oops)