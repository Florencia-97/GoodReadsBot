
import telebot
import requests
import xmltodict
from telebot import types
import re
from collections import OrderedDict 


import os
# BOT_TOKEN = os.environ["BOT_GOOD_READS_TOKEN"]
# KEY = os.environ["KEY_GOOD_READS_BOT"]

LARGO_DESCRIPCIONES_MAX = 150
MAX_LIBROS_LISTADOS = 3

bot = telebot.TeleBot(BOT_TOKEN)

def extraer_argumento(i,arg):
	return arg.split()[i:]

@bot.message_handler(commands=['start'])
def send_welcome(message):
	nombre = extraer_argumento(1,message.text)
	bot.reply_to(message, "Bienvenido al bot no oficial de Goodreads!")


@bot.inline_handler(lambda query: len(query.query) > 2)
def default_query(inline_query):
	books_dic = goodreads(inline_query.query)
	results_list=[]	
	i = 1
	for book,info in books_dic.items():
		print(f"Libro: {book}")
		print(f"Info: {info}")
		mostrar = book + '\n' 
		mostrar	+= 'Author: ' + info["autor"] + '\n'
		cant_estrellas = int(info["score"][0])
		mostrar	+= 'Rank:  ' + '⭐'*cant_estrellas + ' (' + info["score"] + ')' + '\n'
		mostrar	+= 'Cover: ' + info["imagen"] + '\n'
		mostrar	+= 'GoodRead: ' + info["link"] + '\n'
		mostrar	+= 'Description: ' + info["review"] 
		results_list.append(types.InlineQueryResultArticle(f'{i}', book , types.InputTextMessageContent(mostrar), None, None, True, info["autor"], info["imagen"] ,640, 640))
		i += 1	
	try:	
		bot.answer_inline_query(inline_query.id, results=results_list, cache_time=1)
	except Exception as e:
			print('Error in answer')
			print(e)


def goodreads(libro):
	books = []
	try:
		r = requests.get(f"https://www.goodreads.com/search.xml?key={KEY}&q={libro}")
	except:
		print("Error while requesting books")
	try:
		books = xmltodict.parse(r.content)['GoodreadsResponse']['search']['results']['work']
	except:
		print('Error while parsing books')

	dic_books = {}
	for book in books:
		print("Libro: ")
		print(book)
		try:
			title = book['best_book']['title']
		except:
			continue
		info = {}
		info['score'] = get_score(book['average_rating'])
		info['imagen'] = book['best_book']['image_url']
		info['autor'] = book['best_book']['author']['name']
		id = book['best_book']['id']['#text']
		info['review'], info['link'] =  get_review_and_link(id)
		dic_books[title] = info
		
		if len(dic_books) >= MAX_LIBROS_LISTADOS:
			break

	return dic_books

def get_review_and_link(libro_id):
	try:
		r = requests.get("https://www.goodreads.com/book/show/{}.xml?key=LcLFw9NWm11xXMzNkBDHUQ".format(libro_id))
	except:
		print('Error en request a GoodReads')
	book = xmltodict.parse(r.content)['GoodreadsResponse']['book']
	if not book:
		return
	descripcion = book['description']
	url = book['url']
	descripcion = filtrar_descripcion(descripcion)
	return descripcion, url


def filtrar_descripcion( descripcion ):
	if not descripcion :
		return 'Sin descripción disponible'
	corte = '<br />'
	comienzo = 0
	for i in range(2):
		try:
			pos = descripcion.index(corte)
			comienzo = pos + len(corte)
		except:
			continue
		descripcion = descripcion[comienzo:]
	if len(descripcion) > LARGO_DESCRIPCIONES_MAX:
		descripcion = descripcion[:LARGO_DESCRIPCIONES_MAX]
	descripcion = re.sub(r'<[\s]*\/?\w*[\s]*[\/]?>', '\n', descripcion)
	descripcion = re.sub(r'<\W*i\W*>', '', descripcion)
	descripcion = re.sub(r'<\W*\/i\W*>', '', descripcion)

	return descripcion + '...'

def get_score(score):
	print(f"Score: {score}")
	if score is OrderedDict:
		return score['#text']
	return score


bot.polling()
