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


html = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Красивое письмо</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        .email-container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .header {
            background-color: #4CAF50;
            color: #ffffff;
            text-align: center;
            padding: 20px;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
        }
        .content {
            padding: 20px;
            color: #333333;
        }
        .content p {
            line-height: 1.6;
        }
        .button {
            display: inline-block;
            background-color: #4CAF50;
            color: #ffffff;
            text-decoration: none;
            padding: 12px 24px;
            border-radius: 4px;
            margin: 20px 0;
        }
        .footer {
            background-color: #f4f4f4;
            text-align: center;
            padding: 10px;
            font-size: 12px;
            color: #777777;
        }
    </style>
</head>
<body>
    <div class="email-container">
        <!-- Шапка письма -->
        <div class="header">
            <h1>Добро пожаловать!</h1>
        </div>

        <!-- Основное содержимое -->
        <div class="content">
            <p>Здравствуйте,</p>
            <p>Мы рады приветствовать вас в нашем сервисе. Спасибо за регистрацию! Теперь вы можете воспользоваться всеми преимуществами нашей платформы.</p>
            <p>Если у вас есть вопросы, не стесняйтесь обращаться в нашу службу поддержки.</p>
            <a href="https://example.com" class="button">Перейти в личный кабинет</a>
        </div>

        <!-- Футер -->
        <div class="footer">
            <p>Это письмо отправлено автоматически. Пожалуйста, не отвечайте на него.</p>
            <p>© 2023 Ваш Сервис. Все права защищены.</p>
        </div>
    </div>
</body>
</html>
"""
# Тестовое сообщение в виде словаря
test_message = {"to_user_email": "oleg.gregorev.2003@mail.ru", "title": "BimBimbamdddbam", "body": "html"}

# Сериализация сообщения в JSON-строку
message_json = json.dumps(test_message)

# Отправка сообщения в топик
producer.produce(
    topic='notifications_mails',  # Имя топика
    value=message_json.encode('utf-8'),  # Преобразование JSON-строки в байты
    callback=delivery_report,  # Обратный вызов для подтверждения доставки
)

# Ожидание завершения отправки
producer.flush()
