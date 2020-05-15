import logging

import pymongo

from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Database handler
def db_find_book(title):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client['books-db']
    books = database['books']
    students = database['students']
    book = books.find_one({"title": title})
    student_names = []
    if book is not None:
        student_ids = book["students"]
        for id in student_ids:
            student_names.append(students.find_one({"_id": id})["name"])
    client.close()
    return student_names


# Conversation states
SELECTING_ACTION, FINDING_BOOK, ADDING_BOOK, RATING_BOOK, FOUND_BOOK = map(str, range(5))

# End state
END = ConversationHandler.END

def start(update, context):
    """Select an action"""
    
    buttons = [[
        InlineKeyboardButton(text='Find Book', callback_data=str(FINDING_BOOK)),
        InlineKeyboardButton(text='Add Book', callback_data=str(ADDING_BOOK))
    ], [
        InlineKeyboardButton(text='Rate Book', callback_data=str(RATING_BOOK)),
        InlineKeyboardButton(text='Done', callback_data=str(END))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)

    text = 'You may search for a book, add a book or rate a book. To abort, simply type /stop.'

    update.message.reply_text(text=text, reply_markup=keyboard)

    return SELECTING_ACTION

def find_book(update, context):

    update.callback_query.answer()

    text = 'Please type the name of the book.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    return FINDING_BOOK

def found_book(update, context):
    book_title = update.message.text
    student_names = db_find_book(book_title)
    if len(student_names) > 0:
        text = "The following people have the book you are looking for:\n"
        for name in student_names:
            text = text + name + "\n"
    else:
        text = "Sorry, no one has the book you are looking for."
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return END

def add_book(update, context):
    """End conversation from InlineKeyboardButton."""
    update.callback_query.answer()

    text = 'See you around!'
    update.callback_query.edit_message_text(text=text)

    return END

def rate_book(update, context):
    """End conversation from InlineKeyboardButton."""
    update.callback_query.answer()

    text = 'See you around!'
    update.callback_query.edit_message_text(text=text)

    return END


def end(update, context):
    """End conversation from InlineKeyboardButton."""
    update.callback_query.answer()

    text = 'See you around!'
    update.callback_query.edit_message_text(text=text)

    return END

def main():
    # Read token from file
    token_file = open("token.txt")
    token = token_file.readline()
    token_file.close()

    # Get the telegram updater and dispatcher from token
    updater = Updater(token=token, use_context=True)
    dp = updater.dispatcher

    # Set up top level ConversationHandler (selecting action)
    # Because the states of the third level conversation map to the ones of the econd level
    # conversation, we need to make sure the top level conversation can also handle them
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            SELECTING_ACTION: [CallbackQueryHandler(find_book,
                                            pattern='^' + str(FINDING_BOOK) + '$'),
                                CallbackQueryHandler(add_book,
                                            pattern='^' + str(ADDING_BOOK) + '$'),
                                CallbackQueryHandler(rate_book,
                                            pattern='^' + str(RATING_BOOK) + '$'),
                                CallbackQueryHandler(end,
                                            pattern='^' + str(END) + '$')],
            FINDING_BOOK: [MessageHandler(Filters.text, found_book)],
            ADDING_BOOK: [MessageHandler(Filters.text, end)],
            RATING_BOOK: [MessageHandler(Filters.text, end)],
        },

        fallbacks=[CommandHandler('stop', end)],
    )

    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    print("Started!!!!")

    updater.idle()

if __name__ == '__main__':
    main()