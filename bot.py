from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import configparser
from km import KmManager
import log4p

logger = log4p.GetLogger("TelegramBot")
log = logger.logger
config = configparser.ConfigParser()
config.read('credential.config')

kmManager = KmManager()
FULL_TIME='full'
HALF_TIME='half'
OFF_TIME='off'
updater = Updater(config['TELEGRAM']['BotToken'])
print('Bot is Running')

# Commands functions
def help(update: Update, context: CallbackContext) -> None:
    helper = f'''
Hello {update.effective_user.first_name} !

You can use this 3 commands :

- /km <nb total kilometers>
- /bank <new credit/debit>
- /atWork

Thanks for using my bot :)
    '''
    update.message.reply_text(helper)

def km(update: Update, context: CallbackContext) -> None:
    nbKm = update.message.text[3:]
    date = update.message.date
    if(kmManager.addEntry(str(date), str(nbKm))):
        line = '| ' + str(date) + ' | ' + str(nbKm) + ' |'
        update.message.reply_text(line)
    else:
        update.message.reply_text("Tu sais pas écrire mec !")

#@updater.message_handler(commands=['atWork'])
def atWork(update: Update, _: CallbackContext) -> None:
    # Journée entière
    # Demi-journée
    # Absent
    keyboard = [
        [InlineKeyboardButton("Journée entière", callback_data=FULL_TIME)],
        [InlineKeyboardButton("Demi-Journée", callback_data=HALF_TIME)],
        [InlineKeyboardButton("Absent", callback_data=OFF_TIME)],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Open keyboard', reply_markup=reply_markup)

#@updater.callback_query_handler(func=DetailedTelegramCalendar.func())
def atWorkSelected(update: Update, _: CallbackContext)-> None:
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    switcher = {
        FULL_TIME: "Bravo tu as bossé toute la journée, je suis fière de toi.",
        HALF_TIME: "C'est déjà bien une demi-journée.",
        OFF_TIME: "Un peu de repos ne fait pas de mal"
    }
    response = switcher.get(query.data, "Invalid data")
    query.edit_message_text(text=response)
    print("Hey, on est bien passé la :)")
    # Call Google Sheet Service to send date and response

def sendTesteMessage() -> None:
    updater.send_message()



# Commands definition
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('km', km))
updater.dispatcher.add_handler(CommandHandler('bank', km))
updater.dispatcher.add_handler(CommandHandler('atWork', atWork))
#updater.dispatcher.add_handler(CallbackQueryHandler(atWorkSelected))


updater.start_polling()
updater.idle()

print('')
print('Bot stopped')
