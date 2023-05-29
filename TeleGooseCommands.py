import telebot
from telebot import types 
import TeleGooseFunctions
 
TOKEN = "5677194448:AAHZ1vNlvaPFe7zKa0rn-hD5dmVZiGRL0VE"

def getInlineKeyboard() -> types.InlineKeyboardMarkup:
  inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
  
  inline_button1 = types.InlineKeyboardButton(text='My creator\'s YouTube channel', url='https://www.youtube.com/@programmingsimp5596/videos')
  
  button1 = types.InlineKeyboardButton("Info", callback_data="button1")
  
  inline_keyboard.add(inline_button1, button1)
  
  return inline_keyboard

def TeleGooseRun() -> None:

  bot = telebot.TeleBot(TOKEN)
  
  inline_keyboard = getInlineKeyboard()
  
  @bot.message_handler(commands=['start'])
  def start(message) -> None:
    bot.send_message(message.chat.id, "Hello! 🦆\nI am TeleGoose! 🦆\nYou can use the /help function in order to see what can I do! 🦆\n")
   
  @bot.message_handler(commands=['help'])
  def help(message) -> None:
    context = ''
    context += "🦆 /help - list of all the commands.\n\n"
    context += "🦆 /roll - sends random number from 1 up to 6.\n\n"
    context += "🦆 /keyboard - gives you an access to a keyboard with some functions and links.\n\n"
    context += "🦆 /freerooms <HOUR> - sends the free rooms in Atid Lod High School for Sciences at current date and hour.\n\n"
    context += "🦆 also I know to do basic math with plus and minus :)\n\n"
    
    bot.send_message(message.chat.id, context)

  @bot.message_handler(commands=['roll'])
  def rollResponse(message) -> None:
    roll = TeleGooseFunctions.roll(1, 6) 
    bot.send_message(message.chat.id, str(roll)+TeleGooseFunctions.rollToDice(roll))
    
  @bot.message_handler(commands=['keyboard'])
  def activateInlineKeyboard(message) -> None:
    bot.send_message(message.chat.id, 'Here is the inline keyboard!', reply_markup=inline_keyboard)
    
  @bot.message_handler(commands=['freerooms'])
  def send_free_rooms(message) -> None:
    hour = message.text[len('/freerooms'):]
    print("Searching for free rooms...")
    bot.send_message(message.chat.id, "Searching for free rooms... 🦆")
    
    free_rooms = TeleGooseFunctions.get_free_rooms(hour)
    
    if len(free_rooms) == 0:
      bot.send_message(message.chat.id, "No free rooms found or an error ocurred due to invalid input... 🦆")
    
    else:
      free_rooms_message = 'Free rooms found for lesson number ' + hour + ':\n'
      
      for free_room in free_rooms:
        free_rooms_message += '🦆 '+str(free_room)+"\n"
    
      bot.send_message(message.chat.id, free_rooms_message)
    
  @bot.callback_query_handler(func=lambda callback: callback.data)
  def checkCallbackData(callback) -> None:
    if callback.data == 'button1':
      bot.send_message(callback.message.chat.id, 'I was created by Gavriel Linoy in 2023. 🦆')
    
  @bot.message_handler(chat_types=['private', 'group'], func=lambda x: x.text!='')
  def response(message) -> None:
    print(message.from_user.username ,'sent:"',message.text+'"',"in:",message.chat.title)

    lower_message = message.text.lower()
    
    if 'hello' in lower_message:
      bot.send_message(message.chat.id, "Hello there! 🦆")
      
    elif '+' in lower_message or '-' in lower_message:
      bot.send_message(message.chat.id, TeleGooseFunctions.solveMath(lower_message))
      
    else: 
      bot.send_message(message.chat.id, message.text+' 🦆')
  
  @bot.message_handler(content_types=['sticker'])
  def contentResponse(message) -> None:
    bot.send_sticker(message.chat.id, sticker='CAACAgQAAxkBAAEHckhj0Y7K7bKkJJnRHm3YVJ4FzXE7bAAC0wkAApExsFMGqypb2VqbhC0E')

  bot.polling()