from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = "5783163714:AAG8l0GKFCzcGyGjw7QBxgVtQGaKwov-OgM"  # Забираем значение типа str
ADMINS = ["749333822"]  # Тут у нас будет список из админов
IP = "192.168.0.1"  # Тоже str, но для айпи адреса хоста

