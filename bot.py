
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

@bot.inline_handler(lambda query: len(query.query) > 1)
def default_query(inline_query):
	list = []
	titulo, score, imagen, review, link, autor = goodreads(inline_query.query)
	mostrar = titulo + '\n' + 'Author: ' + autor + '\n' + 'Rank:  ' + score + '\n' + 'Cover: ' + imagen + '\n' + 'Link: ' + link + '\n' + 'Description: ' + review + '...'
	try:
		list.append(types.InlineQueryResultArticle('1', titulo , types.InputTextMessageContent(mostrar)))
		bot.answer_inline_query(inline_query.id, list)
	except Exception as e:
		print('Error in answer')


def goodreads(libro):
	r = requests.get("https://www.goodreads.com/search.xml?key=LcLFw9NWm11xXMzNkBDHUQ&q={}".format(str(libro)))
	list = []
	try:
		book = xmltodict.parse(r.content)['GoodreadsResponse']['search']['results']['work'][0]
	except:
		print('request error')
	title = book['best_book']['title']
	score = book['average_rating']
	imagen = book['best_book']['image_url']
	id = book['best_book']['id']['#text']
	autor = book['best_book']['author']['name']
	review, link =  get_review_and_link(id)
	return title,score,imagen,review,link, autor


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
	descripcion = descripcion.replace("<i>","")
	descripcion = descripcion.replace("</i>","")
	descripcion.replace("<br /><br />", "\n")
	return descripcion
bot.polling()
