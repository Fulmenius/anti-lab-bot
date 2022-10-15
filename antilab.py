import telebot
import datetime
import numpy as np
from matplotlib import pyplot as plt 
import re
import os
import ast
from telebot import types 


TOKEN = '1162569758:AAGzw0zP9oFCA6_JDaBrGyy03x05m11MAwQ'

bot = telebot.TeleBot(TOKEN)


users = {}						# dict with userdata
for i in os.listdir('./userdata'):
	users[str(i)] = str(i)


def options_list(path, chat_id): #takes a path to a folder, 
#lists the folder's content in a form of a list of options
	options = []
	markup = telebot.types.InlineKeyboardMarkup()
	for i in os.listdir(path):
		options.append(telebot.types.InlineKeyboardButton(text=str(i), callback_data=str(i)))

	if len(options) == 0:
		bot.send_message(chat_id=chat_id, text="Извините, в этом разделе ещё нет готовых шаблонов.")

	else:
		for o in options:
			markup.add(o)

		bot.send_message(chat_id=chat_id, text="Выберите шаблон", reply_markup=markup)	



@bot.message_handler(commands=['start'])  
def start_handler(message):
	markup = telebot.types.InlineKeyboardMarkup()
	otc = telebot.types.InlineKeyboardButton(text='Сделать отчёт', callback_data='tex')
	graph = telebot.types.InlineKeyboardButton(text='Построить график', callback_data='graph') 
	markup.add(otc)
	markup.add(graph)
	bot.send_message(chat_id=message.chat.id, text="Привет. Я - Антилабник.", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
	if call.data == 'tex':
		markup = telebot.types.InlineKeyboardMarkup()
		i = telebot.types.InlineKeyboardButton(text='I курс', callback_data='I')
		ii = telebot.types.InlineKeyboardButton(text='II курс', callback_data='II')
		iii = telebot.types.InlineKeyboardButton(text='III курс', callback_data='III')
		iv = telebot.types.InlineKeyboardButton(text='IV курс', callback_data='IV')
		markup.add(i)
		markup.add(ii)
		markup.add(iii)
		markup.add(iv)
		bot.send_message(chat_id=call.from_user.id, text="Выбери курс", reply_markup=markup)

	elif call.data == 'graph':
		bot.send_message(chat_id=call.from_user.id, text='Эта функция пока недоступна')

	elif call.data == 'I':
		options_list('./templates/I', call.from_user.id)

	elif call.data == 'II':
		options_list('./templates/II', call.from_user.id)

	elif call.data == 'III':
		options_list('./templates/III', call.from_user.id)

	elif call.data == 'IV':
		options_list('./templates/IV', call.from_user.id)
	
	else:
		try:
			bot.send_message(chat_id=call.from_user.id, text="Выбран шаблон " + str(call.data))		
		except:
			bot.send_message(chat_id=call.from_user.id, text="Произошла ошибка")		

@bot.message_handler(commands=['help'])
def help_handler(message):
	bot.send_message(message.from_user.id, "Тут будет инструкция")


def save_image(message, u_id):
		photo = message.photo[-1]
		file_id = photo.file_id
		file_path = bot.get_file(file_id).file_path
		downloaded_file = bot.download_file(file_path)
		name = file_id + ".jpg"
		new_file = open('./userdata/' + str(u_id) + '/' + name, mode = 'wb')
		new_file.write(downloaded_file)
		new_file.close()

def save_data(message, u_id):
	file_name = message.document.file_name
	file_info = bot.get_file(message.document.file_id) 
	file = bot.download_file(file_info.file_path)
	src = file_name
	new_data = open('./userdata/' + str(u_id) + '/' + file_name, mode = 'wb')
	new_data.write(file)
	new_data.close()
		

@bot.message_handler(content_types=['document'])
def photo_handler(message):
	u_id = message.from_user.id

	if str(u_id) in users:
		save_data(message, u_id)
		bot.send_message(u_id, "Welcome back. Your data is saved")
		
	else:	
		users[str(u_id)] = [str(u_id)]
		os.mkdir('./userdata/' + str(u_id))
		save_data(message, u_id)
		bot.send_message(u_id, "Welcome to the club")


@bot.message_handler(func=lambda m: True)
def something_else(message):
	bot.send_message(message.from_user.id, 'Ты набрал что-то не то')



bot.polling()


