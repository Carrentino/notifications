from confluent_kafka import Producer
import json

# Конфигурация Kafka producer
conf = {
    'bootstrap.servers': 'localhost:9092',  # Адрес Kafka-брокера
}

# Создание producer
producer = Producer(conf)


# Функция для обработки подтверждений доставки
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


# Тестовое сообщение в виде словаря
test_message = {
    "to_user": "4e3ea803-e1da-46d6-972f-d6d495442066",
    "title": "Test Push Notification",
    "body": "This is a test message from Kafka!",
}

# Сериализация сообщения в JSON-строку
message_json = json.dumps(test_message)

# Отправка сообщения в топик
producer.produce(
    topic='notifications_pushes',  # Имя топика
    value=message_json.encode('utf-8'),  # Преобразование JSON-строки в байты
    callback=delivery_report,  # Обратный вызов для подтверждения доставки
)

# Ожидание завершения отправки
producer.flush()
