import telebot
import os
from googletrans import Translator
import speech_recognition as sr
from pydub import AudioSegment

# Замените на свой токен
TOKEN = '7823042550:AAFfymkQbbw2McKHJGBn8PRYScVwrtqRUho'
bot = telebot.TeleBot(TOKEN)
translator = Translator()

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    try:
        # Получаем файл
        file_info = bot.get_file(message.voice.file_id)
        file = bot.download_file(file_info.file_path)

        ogg_filename = f"voice_{message.message_id}.ogg"
        wav_filename = f"voice_{message.message_id}.wav"

        # Сохраняем OGG файл
        with open(ogg_filename, 'wb') as f:
            f.write(file)

        # Конвертируем OGG в WAV
        sound = AudioSegment.from_ogg(ogg_filename)
        sound.export(wav_filename, format="wav")

        # Распознаем речь
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_filename) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language="ru-RU")

        # Перевод
        translated = translator.translate(text, dest='en')

        # Отправка ответа
        response = f"🗣 Распознано: {text}\n\n🌐 Перевод: {translated.text}"
        bot.send_message(message.chat.id, response)

    except sr.UnknownValueError:
        bot.send_message(message.chat.id, "Не удалось распознать речь.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")
    finally:
        # Очистка временных файлов
        if os.path.exists(ogg_filename):
            os.remove(ogg_filename)
        if os.path.exists(wav_filename):
            os.remove(wav_filename)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Отправь голосовое сообщение, и я переведу его на английский!")

print("Бот запущен.")
bot.infinity_polling()
