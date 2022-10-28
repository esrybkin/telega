from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from game import *


app = ApplicationBuilder().token("___").build()

app.add_handler(CommandHandler("Help", help_command))
app.add_handler(CommandHandler("Start", start_command))
app.add_handler(CommandHandler("Rules", rules_command))

print('Server is running...')
app.run_polling()
