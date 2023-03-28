from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
from django.core.management import BaseCommand
from bot.views import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        updater = Updater("6244919959:AAH98ylnVENOm6mF7WFwIF2Ah8-ayMzY_y4")
        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, received_message))
        updater.dispatcher.add_handler(CallbackQueryHandler(callback))
        updater.start_polling()
        updater.idle()