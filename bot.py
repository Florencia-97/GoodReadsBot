
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
	bot.reply_to(message, nombre +  " Howdy, how are you doing?")

@bot.message_handler(commands=['buscar'])
def search(message):
	nombre_ingresado = extraer_argumento(1,message.text)
	libro = ""
	for palabra in nombre_ingresado:
		libro += palabra + '+'
	titulo, score, imagen = goodreads(libro[:-1].encode('utf-8').strip())
	bot.reply_to(message, titulo + '\n' + score + '\n' + imagen)


def goodreads(libro):
	r = requests.get("https://www.goodreads.com/search.xml?key=LcLFw9NWm11xXMzNkBDHUQ&q={}".format(str(libro)))
	try:
		title = xmltodict.parse(r.content)['GoodreadsResponse']['search']['results']['work'][0]['best_book']['title']
	except:
		print("hola")
	score = xmltodict.parse(r.content)['GoodreadsResponse']['search']['results']['work'][0]['average_rating']
	imagen = xmltodict.parse(r.content)['GoodreadsResponse']['search']['results']['work'][0]['best_book']['image_url']
	return title, score, imagen


bot.polling()
