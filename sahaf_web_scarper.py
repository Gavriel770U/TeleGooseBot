# requirements:
# venv
# pip install selenium 

from enum import Enum
from selenium import webdriver 
from selenium.webdriver.common.by import By
import datetime
import time

INC = 1
DEC = 1
DAYS_AMOUNT = 5

CURRENT_ROOM_IS_FREE = 770

# ClassLabel.value tuple constants
CLASS_NAME_INDEX = 0 
CLASS_OPTION_VALUE_INDEX = 1

# get_occupied_rooms function constants
DATE_TD_INC = 2
TD_INC = 1
TR_INC = 2

# current year 
CURRENT_YEAR = datetime.datetime.now().strftime(".%Y")

class ClassLabel(Enum):
  # ClassLabel.value tuple structure -> (class_name: str, class_option_value: int)
  
  TET1 = ("ט - 1", 1)
  TET2 = ("ט - 2", 2)
  TET3 = ("ט - 3", 3)
  TET4 = ("ט - 4", 4)
  TET5 = ("ט - 5", 5)
  
  YOD1 = ("י - 1", 6)
  YOD2 = ("י - 2", 7)
  YOD3 = ("י - 3", 8)
  YOD4 = ("י - 4", 9)
  YOD5 = ("י - 5", 10)
  
  YODA1 = ("יא - 1", 11)
  YODA2 = ("יא - 2", 12)
  YODA3 = ("יא - 3", 13)
  YODA4 = ("יא - 4", 14)
  YODA5 = ("יא - 5", 15)
  YODA6 = ("יא - 6", 16)
  
  YODB1 = ("יב - 1", 17)
  YODB2 = ("יב - 2", 18)
  YODB3 = ("יב - 3", 19)
  YODB4 = ("יב - 4", 20)
  YODB5 = ("יב - 5", 21)
  YODB6 = ("יב - 6", 22)

def click_on_schedule(driver) -> None:
  """
  Function that clicks on the Shahaf schedule and by that opens it.
  :param driver: selenium webdriver
  :type driver: webdriver.any 
  :return: None
  :rtype: None
  """
  
  schedule_button = driver.find_element(By.XPATH, '//*[@id="dnn_ctr1319_TimeTableView_btnTimeTable"]')
  schedule_button.click()

def click_on_changes(driver) -> None:
  """
  Function that clicks on the Shahaf schedule changes and by that opens it.
  :param driver: selenium webdriver
  :type driver: webdriver.any 
  :return: None
  :rtype: None
  """
  
  changes_button = driver.find_element(By.XPATH, '//*[@id="dnn_ctr1319_TimeTableView_btnChanges"]')
  changes_button.click() 

def click_choose_class(driver, chosen_class: ClassLabel) -> None:
  """
  Function that clicks on specific class schedule that is given as parameter
  :param driver: selenium webdriver
  :type driver: webdriver.any
  :param chosen_class: a class to choose its schedule 
  :type chosen_class: ClassLabel 
  :return: None
  :rtype: None 
  """
  
  class_choice_button = driver.find_element(By.XPATH, '//*[@id="dnn_ctr1319_TimeTableView_ClassesList"]')
  class_choice_button.click()
  
  class_choice_xpath_base = '//*[@id="dnn_ctr1319_TimeTableView_ClassesList"]/option['
  class_choice_xpath_base += str(chosen_class.value[CLASS_OPTION_VALUE_INDEX])
  class_choice_xpath_base += ']'
  
  class_choice = driver.find_element(By.XPATH, class_choice_xpath_base)
  class_choice.click()

def get_occupied_rooms(driver, date: str, lesson_number: int) -> list: 
  """
  :param driver: selenium webdriver 
  :type driver: webdriver.any 
  :param date: a date to search occupied rooms
  :type date: str
  :param lesson_number: the lesson number to search occupied rooms
  :type lesson_number: int
  :return: a list of int numbers that represents the occupied rooms at this lesson and date, in the current chosen class schedule
  :rtype: list
  """
  
  day_counter = 0
  
  # finds current day value using site data
  for day_value in range(DAYS_AMOUNT):
    day_counter+=INC
    day_base_x_path = '//*[@id="dnn_ctr1319_TimeTableView_PlaceHolder"]/div/table/tbody/tr[1]/td['
    day_base_x_path += str(day_value+DATE_TD_INC)
    day_base_x_path += ']'
    
    data = driver.find_element(By.XPATH, day_base_x_path).text
    
    if date in data:
      break 
  
  # finds all occupied rooms at given hour and day
  data_xpath = '//*[@id="dnn_ctr1319_TimeTableView_PlaceHolder"]/div/table/tbody/tr['
  data_xpath += str(lesson_number + TR_INC)
  data_xpath += ']/td['
  data_xpath += str(day_counter + TD_INC)
  data_xpath += ']'
  
  data = driver.find_element(By.XPATH, data_xpath).text
  splited_data = data.split('(ח')
  occupied_rooms = []

  for data in splited_data:
    if ')' in data:
      data = data[:data.find(')')]
      if not 'חינוך גופני' in data and not 'אודיטוריום' in data:
        occupied_rooms.append(int(data))
  
  return occupied_rooms

# TODO 
# FIXME
def get_occupied_or_free_room_by_changes(driver, date: str, lesson_number: int) -> tuple:
  """
  returns (new_occupied_room_number, is_current_room_free_now)
  :param driver: selenium webdriver
  :type driver: webdriver.any
  :param date: 
  :type date: str
  :param lesson_number:
  :type lesson_number: int
  :return: 
  :rtype: 
  """
  
  is_current_room_free_now = 0
  new_occupied_room_number = 0
  
  change_index = 1
  next_date = (datetime.datetime.strptime(date+CURRENT_YEAR, '%d.%m.%Y') + datetime.timedelta(days=1)).strftime("%d.%m.%Y")
  running_no_date_issues = True

  while running_no_date_issues:
    base_room_change_data_xpath = '//*[@id="dnn_ctr1319_TimeTableView_PlaceHolder"]/div/table/tbody/tr['
    base_room_change_data_xpath += str(change_index)
    base_room_change_data_xpath += ']/td'
    
    try:
      room_change_data = driver.find_element(By.XPATH, base_room_change_data_xpath).text
    except Exception:
      break
    
    room_change_date = room_change_data[:5]
    
    if 'תגבור' in room_change_data:
      room_change_lesson_number = int(room_change_data[26])
    else:
      room_change_lesson_number = int(room_change_data[18])
      
    date_compare1 = datetime.datetime.strptime(date, '%d.%m')
    date_compare2 = datetime.datetime.strptime(room_change_date, '%d.%m')
      
    if date_compare1 == date_compare2: 
      # check for changes, additional lessons,  
      if room_change_lesson_number == lesson_number:
        if 'תגבור' in room_change_data or 'החלפת חדר' in room_change_data:
          splited_info = room_change_data.split(' ')
          new_occupied_room_number = int(splited_info[-1][1:])
        elif 'ביטול שיעור' in room_change_data:
          is_current_room_free_now = CURRENT_ROOM_IS_FREE
        
          
    elif date_compare1 < date_compare2:
      # if the destition date is passed the program will end searching for more free rooms
      running_no_date_issues = False 
    
    # update value for xpath index
    change_index+=INC
  
  return (new_occupied_room_number, is_current_room_free_now)

def parse_with_changes() -> list:
  url = 'https://alehlod.iscool.co.il/default.aspx'
  current_date = datetime.datetime.now().strftime("%d.%m")
  
  lesson_number = int(input("Enter hour to get its free rooms: "))
  
  classes = [
    ClassLabel.TET1, ClassLabel.TET2, ClassLabel.TET3, ClassLabel.TET4, ClassLabel.TET5, 
    ClassLabel.YOD1, ClassLabel.YOD2, ClassLabel.YOD3, ClassLabel.YOD4, ClassLabel.YOD5, 
    ClassLabel.YODA1, ClassLabel.YODA2, ClassLabel.YODA3, ClassLabel.YODA4, ClassLabel.YODA5, ClassLabel.YODA6, 
    ClassLabel.YODB1, ClassLabel.YODB2, ClassLabel.YODB3, ClassLabel.YOD4, ClassLabel.YODB5, ClassLabel.YODB6
  ]
  
  all_rooms = [1, 2, 3, 4, 5, 6, 7, 8, 9, 15, 16, 17, 18, 21, 22, 23, 26, 30, 31, 32, 33, 34, 35, 36, 37]
  banned_rooms = [] #[23, 31]
  # initialize current free rooms 
  free_rooms = [room_number for room_number in all_rooms if room_number not in banned_rooms] 
  
  driver = webdriver.Chrome()
  driver.maximize_window()
  driver.get(url)
    
  for classLabel in classes:
    click_on_schedule(driver)
    time.sleep(0.5)
    click_choose_class(driver, classLabel)
    time.sleep(0.5)
    occupied_rooms = get_occupied_rooms(driver, current_date, lesson_number)
    click_on_changes(driver)
    time.sleep(1)
    new_occupied_room_number, is_current_room_free_now = get_occupied_or_free_room_by_changes(driver, current_date, lesson_number)
    
    for occupied_room in occupied_rooms:
      if CURRENT_ROOM_IS_FREE != is_current_room_free_now and new_occupied_room_number != 0:
        free_rooms.remove(new_occupied_room_number)   
      elif CURRENT_ROOM_IS_FREE != is_current_room_free_now and occupied_room in free_rooms: 
        free_rooms.remove(occupied_room)
    time.sleep(1)

  driver.close()
  return free_rooms

def main() -> None:
  print(parse_with_changes())

if __name__ == "__main__":
  main()