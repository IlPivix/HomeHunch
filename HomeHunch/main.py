import telebot
import joblib
import pandas as pd
from telebot import types

bot = telebot.TeleBot("6068104901:AAHT2bSF-F_TPiE-e4rvb1WQjJsmlkRWcZw")
fase = 0
domande = ["quante camere da letto ha?", "quanti bagni ha?", "quanti piani ha?", "è vicina al mare? (1: si, 0: no)", "ha una vista panoramica? (valore da 0 a 4)", "condizione generale della casa (da 1 a 5)",
           "valutazione generale della costruzione e del design della casa (da 1 a 13)","superficie abitabile (piedi quadrati) al di sopra del livello del suolo", "ha un seminterrato? (1: si, 0: no)",
           "in che anno è stata costruita?", "è mai stata ristrutturata? (1: si, 0: no)", "codice postale", "latitudine", "longitudine", "la superficie abitabile è maggiore alla media della zona? (1: si, 0: no)",
           "la superficie del terreno è maggiore alla media della zona? (1: si, 0: no)"]
risposte = []

@bot.message_handler(commands =["start"])
def start(message):
    global fase
    fase = 0
    btnSi = types.InlineKeyboardButton('SI!', callback_data='si')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(btnSi)
    bot.send_message(message.chat.id, "Ciao! Sono HomeHunch e ti aiuterò a stimare il prezzo del tuo immobile, sei pronto?", reply_markup=keyboard)

@bot.callback_query_handler(func=None)
def handle_button_press(call):
    global fase
    if call.data == 'si':
        fase = 0
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=types.InlineKeyboardMarkup())
        bot.send_message(chat_id=call.message.chat.id, text="Per interrompere in qualsiasi momento il procedimento usa /quit, ricorda di usare il punto al posto della virgola")
        bot.send_message(chat_id=call.message.chat.id, text=domande[fase])
        fase += 1

@bot.message_handler(commands =["quit"])
def quit(message):
    global risposte
    global fase
    if fase != 0:
        bot.send_message(chat_id=message.chat.id, text="Processo interrotto!")
        fase = 0
        risposte.clear()
    else:
        bot.send_message(chat_id=message.chat.id, text="Non è stato iniziato nessun processo!")

@bot.message_handler(func=lambda message: True)
def messageReceived(message):
    global fase
    check = message.text.replace(".", "")
    check1 = check.replace("-", "")
    if fase == len(domande) and check1.isnumeric():
        numero = float(message.text)
        risposte.append(numero)
        model = joblib.load("houseData.joblib")
        nuovi_dati = pd.DataFrame(
                {'bedrooms': [risposte[0]], 'bathrooms': [risposte[1]], 'floors': [risposte[2]], 'waterfront': [risposte[3]], 'view': [risposte[4]], 'condition': [risposte[5]],
                 'grade': [risposte[6]], 'sqft_above': [risposte[7]], 'has_basement': [risposte[8]], 'yr_built': [risposte[9]], 'has_been_renovated': [risposte[10]],
                 'zipcode': [risposte[11]], 'lat': [risposte[12]], 'long': [risposte[13]], 'sqft_living_med': [risposte[14]], 'sqft_lot_med': [risposte[15]]})
        prediction = model.predict(nuovi_dati)
        bot.send_message(chat_id=message.chat.id, text=f"Grazie per aver fornito i dati necessari! La previsione per questo immobile è: {int(prediction[0])}€")
        fase=0
    elif fase != 0 and check1.isnumeric():
        numero = float(message.text)
        if fase < len(domande):
            if fase == 1:
                if numero > 0:
                    risposte.append(numero)
                    bot.send_message(chat_id=message.chat.id, text=domande[fase])
                    fase += 1
                else:
                    bot.send_message(chat_id=message.chat.id, text="Hey! Una casa deve avere almeno una camera da letto")
            elif fase == 2:
                if numero > 0:
                    risposte.append(numero)
                    bot.send_message(chat_id=message.chat.id, text=domande[fase])
                    fase += 1
                else:
                    bot.send_message(chat_id=message.chat.id, text="Hey! Una casa deve avere almeno un bagno")
            elif fase == 3:
                if numero > 0:
                    risposte.append(numero)
                    bot.send_message(chat_id=message.chat.id, text=domande[fase])
                    fase += 1
                else:
                    bot.send_message(chat_id=message.chat.id, text="Hey! Una casa deve avere almeno un piano")
            elif fase == 4:
                if numero == 0 or numero == 1:
                    risposte.append(numero)
                    bot.send_message(chat_id=message.chat.id, text=domande[fase])
                    fase += 1
                else:
                    bot.send_message(chat_id=message.chat.id, text="Hey! I valori ammessi sono 0 e 1")
            elif fase == 5:
                if numero >= 0 and numero <= 4:
                    risposte.append(numero)
                    bot.send_message(chat_id=message.chat.id, text=domande[fase])
                    fase += 1
                else:
                    bot.send_message(chat_id=message.chat.id, text="Hey! I valori ammessi sono da 0 a 4")
            elif fase == 6:
                if numero >= 1 and numero <= 5:
                    risposte.append(numero)
                    bot.send_message(chat_id=message.chat.id, text=domande[fase])
                    fase += 1
                else:
                    bot.send_message(chat_id=message.chat.id, text="Hey! I valori ammessi sono da 1 a 5")
            elif fase == 7:
                if numero >= 1 and numero <= 13:
                    risposte.append(numero)
                    bot.send_message(chat_id=message.chat.id, text=domande[fase])
                    fase += 1
                else:
                    bot.send_message(chat_id=message.chat.id, text="Hey! I valori ammessi sono da 1 a 13")
            elif fase == 8:
                if numero > 0:
                    risposte.append(numero)
                    bot.send_message(chat_id=message.chat.id, text=domande[fase])
                    fase += 1
                else:
                    bot.send_message(chat_id=message.chat.id, text="Hey! Una casa non può avere superficie negativa")
            elif fase == 9:
                if numero == 0 or numero == 1:
                    risposte.append(numero)
                    bot.send_message(chat_id=message.chat.id, text=domande[fase])
                    fase += 1
                else:
                    bot.send_message(chat_id=message.chat.id, text="Hey! I valori ammessi sono 0 e 1")
            elif fase == 10:
                if numero > 0:
                    risposte.append(numero)
                    bot.send_message(chat_id=message.chat.id, text=domande[fase])
                    fase += 1
                else:
                    bot.send_message(chat_id=message.chat.id, text="Hey! L'anno non può essere negativo")
            elif fase == 11:
                if numero == 0 or numero == 1:
                    risposte.append(numero)
                    bot.send_message(chat_id=message.chat.id, text=domande[fase])
                    fase += 1
                else:
                    bot.send_message(chat_id=message.chat.id, text="Hey! I valori ammessi sono 0 e 1")
            elif fase == 12:
                if numero > 0:
                    risposte.append(numero)
                    bot.send_message(chat_id=message.chat.id, text=domande[fase])
                    fase += 1
                else:
                    bot.send_message(chat_id=message.chat.id, text="Hey! Il codice postale non può essere negativo")
            elif fase == 15:
                if numero == 0 or numero == 1:
                    risposte.append(numero)
                    bot.send_message(chat_id=message.chat.id, text=domande[fase])
                    fase += 1
                else:
                    bot.send_message(chat_id=message.chat.id, text="Hey! I valori ammessi sono 0 e 1")
            elif fase == 16:
                if numero == 0 or numero == 1:
                    risposte.append(numero)
                    bot.send_message(chat_id=message.chat.id, text=domande[fase])
                    fase += 1
                else:
                    bot.send_message(chat_id=message.chat.id, text="Hey! I valori ammessi sono 0 e 1")
            else:
                risposte.append(numero)
                bot.send_message(chat_id=message.chat.id, text=domande[fase])
                fase += 1
    else:
        bot.send_message(chat_id=message.chat.id, text="Hey! Stai scrivendo cose a caso (inserisci solo numeri senza spazi)")

bot.polling()