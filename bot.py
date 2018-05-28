
import telebot
import requests
import xmltodict
from telebot import types

#goodreads claves
#key: LcLFw9NWm11xXMzNkBDHUQ
#secret: YMav7dE2erXytdnuZx0eXyNbSGFwLjEVG2yjir7Ro

bot_token = '586963462:AAFru_TSEvS5Qyro8dRoJ_leHYDslVCQR5k'

bot = telebot.TeleBot(bot_token)

def extraer_argumento(i,arg):
	return arg.split()[i:]

@bot.message_handler(commands=['start'])
def send_welcome(message):
	nombre = extraer_argumento(1,message.text)
	bot.reply_to(message, "Bienvenido al bot no oficial de Goodreads!")

@bot.message_handler(commands=['buscar'])
def search(message):
	nombre_ingresado = extraer_argumento(1,message.text)
	libro = ""
	for palabra in nombre_ingresado:
		libro += palabra + '+'
	titulo, score, imagen, review, link = goodreads(libro[:-1].encode('utf-8').strip())
	mostrar = titulo + '\n' + 'Rank: ' + score + '\n' + 'Cover: ' + imagen + '\n' + 'Link: ' + link + '\n' + 'Description: ' + review + '...'
	bot.reply_to(message, mostrar)



@bot.inline_handler(lambda query: len(query.query) > 1)
def default_query(inline_query):
	list = []
	titulo, score, imagen, review, link = goodreads('Emma')
	mostrar = titulo + '\n' + 'Rank: ' + score + '\n' + 'Cover: ' + imagen + '\n' + 'Link: ' + link + '\n' + 'Description: ' + review + '...'
	try:
		list.append(types.InlineQueryResultPhoto('1',
                                         'https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png',
                                         'https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png',
										 input_message_content=types.InputTextMessageContent(mostrar)))
		list.append(types.InlineQueryResultArticle('2', inline_query.query , types.InputTextMessageContent('Copyright (c) 2017 Copyright Holder All Rights Reserved.')))
		bot.answer_inline_query(inline_query.id, list)
	except Exception as e:
		print(e)

def get_iq_articles(exchanges):
   result = []
   for exc in exchanges:
       result.append(
           telebot.types.InlineQueryResultArticle(
               id=exc['ccy'],
               title=exc['ccy'],
               input_message_content=telebot.types.InputTextMessageContent(
                   serialize_ex(exc),
                   parse_mode='HTML'
               ),
               reply_markup=get_update_keyboard(exc),
               description='Convert ' + exc['base_ccy'] + ' -> ' + exc['ccy'],
               thumb_height=1
           )
       )
   return result


def goodreads(libro):
	r = requests.get("https://www.goodreads.com/search.xml?key=LcLFw9NWm11xXMzNkBDHUQ&q={}".format(str(libro)))
	try:
		book = xmltodict.parse(r.content)['GoodreadsResponse']['search']['results']['work'][0]
	except:
		print("Errpr")
	title = book['best_book']['title']
	score = book['average_rating']
	imagen = book['best_book']['image_url']
	id = book['best_book']['id']['#text']
	review, link =  get_review_and_link(id)
	return title, score, imagen, review, link

def get_review_and_link(libro_id):
	try:
		r = requests.get("https://www.goodreads.com/book/show/{}.xml?key=LcLFw9NWm11xXMzNkBDHUQ".format(libro_id))
	except:
		print('error')
	book = xmltodict.parse(r.content)['GoodreadsResponse']['book']
	descripcion = book['description']
	url = book['url']
	descripcion = filtrar_descripcion(descripcion)
	return descripcion, url

def filtrar_descripcion(descripcion):
	corte = '<br />'
	for i in range(2):
		try:
			pos = descripcion.index(corte)
			comienzo = pos + len(corte)
		except:
			comienzo = 0
		descripcion = descripcion[comienzo:]
	return descripcion

bot.polling()
