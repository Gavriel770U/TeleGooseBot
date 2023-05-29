import random
import datetime
from sahaf_web_scarper import *
import time

SECONDS = 1

def roll(min, max) -> int:
  return random.randint(min, max)


def rollToDice(value) -> str:
  if value == 1:
    return ' ⚀'
  elif value == 2:
    return ' ⚁'
  elif value == 3:
    return ' ⚂'
  elif value == 4:
    return ' ⚃'
  elif value == 5:
    return ' ⚄'
  else:
    return ' ⚅'


def math(equation) -> int:
  numbers = []
  operators = []
  currentNumber = ''
  res = 0
      
  numbers = []
  currentNumber = ''; 
  operators = []
  for i in equation:
    if (i >= '0' and i <= '9'):
      currentNumber += i
    elif i=='+' or i=='-':
      numbers.append(int(currentNumber))
      operators.append(i)
      currentNumber = ''
  numbers.append(int(currentNumber))
  currentNumber = ''
  
  index = 0 
  res = int(numbers[index])
  
  for i in range(1, len(numbers)):
    operator = operators[index] 
    if operator == '+':
      res += int(numbers[i])
    elif operator == '-':
      res -= int(numbers[i])
    index += 1 
    
  return res

def solveMath(equation) -> str:
  return str(math(equation))

def get_free_rooms(hour) -> list:
  url = 'https://alehlod.iscool.co.il/default.aspx'
  current_date = datetime.datetime.now().strftime("%d.%m")
  
  try:
    lesson_number = int(hour)
  except Exception:
    return []
  
  classes = [
    ClassLabel.TET1, ClassLabel.TET2, ClassLabel.TET3, ClassLabel.TET4, ClassLabel.TET5, 
    ClassLabel.YOD1, ClassLabel.YOD2, ClassLabel.YOD3, ClassLabel.YOD4, ClassLabel.YOD5, 
    ClassLabel.YODA1, ClassLabel.YODA2, ClassLabel.YODA3, ClassLabel.YODA4, ClassLabel.YODA5, ClassLabel.YODA6, 
    ClassLabel.YODB1, ClassLabel.YODB2, ClassLabel.YODB3, ClassLabel.YOD4, ClassLabel.YODB5, ClassLabel.YODB6
  ]
  
  all_rooms = [1, 2, 3, 4, 5, 6, 7, 8, 9, 15, 16, 17, 18, 21, 22, 23, 26, 30, 31, 32, 33, 34, 35, 36, 37]
  banned_rooms = [23, 31]
  free_rooms = [room_number for room_number in all_rooms if room_number not in banned_rooms]
  
  driver = webdriver.Chrome()
  driver.maximize_window()
  driver.get(url)
  
  click_on_schedule(driver)
  
  for classLabel in classes:
    click_choose_class(driver, classLabel)
    occupied_rooms = get_occupied_rooms(driver, current_date, lesson_number)
    for occupied_room in occupied_rooms:
      if occupied_room in free_rooms:
        free_rooms.remove(occupied_room)
    time.sleep(SECONDS)
  
  driver.close()
      
  return free_rooms
  
#---------------------------------------------------------------------------------------------------------------
 # @bot.message_handler(commands=['keyboard'])
 # def activateKeyboard(message) -> None:
   # global isKeyboardActivated
   # bot.send_message(message.chat.id, 'Here is the keyboard!', reply_markup=keyboard) 
   # isKeyboardActivated = True 
  
  # @bot.message_handler(commands=['deactivate_keyboard'])
  # def deactivateKeyboard(message) -> None:
  #   global isKeyboardActivated 
  #   bot.send_message(message.chat.id, 'Keyboard has been deactivated!', reply_markup=None)
  #   isKeyboardActivated = False 
  
      # if(isKeyboardActivated):
    #   if lowerMessage == 'info':
    #     bot.send_message(message.chat.id, "TeleGoose is a bot that is created by Gavriel Linoy in 2023.")
    #   elif lowerMessage == 'press me!':
    #     bot.send_message(message.chat.id, "Hey! You pressed me~! :)")
    #   return 
    
      #keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)