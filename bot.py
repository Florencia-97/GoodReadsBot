
import telebot
import requests
import xmltodict

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


def goodreads(libro):
	r = requests.get("https://www.goodreads.com/search.xml?key=LcLFw9NWm11xXMzNkBDHUQ&q={}".format(str(libro)))
	try:
		book = xmltodict.parse(r.content)['GoodreadsResponse']['search']['results']['work'][0]
	except:
		print("hola")
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
		print(ola)
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
