import pyautogui
import pandas as pd
import time
import datetime

# Get current time stamp
now = datetime.datetime.now()
timeStamp = now.strftime("%Y-%m-%d")

# Set up auto GUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

# Button locations
newTransaction = (540, 430)
date = (425, 460)
notes = (500, 660)
done = (900, 760)

# Read in CSV data
data = pd.read_csv('data.csv', header = 0)

# Give time for user to navigate to page
print("Load webpage at full size. You have 3 seconds")
for ii in range(3):
    print('.', end='', flush=True)
    time.sleep(1)

# Function for entering data
def createEntry(idx):
     pyautogui.click(newTransaction)

     pyautogui.click(date)
     pyautogui.hotkey('command', 'a')
     pyautogui.press('delete')
     pyautogui.typewrite(data.iat[idx,0])
     pyautogui.press('tab')

     pyautogui.typewrite(data.iat[idx,1])
     pyautogui.press('tab')

     pyautogui.typewrite(data.iat[idx,2])
     pyautogui.press('tab')

     pyautogui.typewrite(str(data.iat[idx,3]))

     pyautogui.click(notes)
     pyautogui.typewrite("Imported on "+ timeStamp)

     pyautogui.click(done)

# Loop through all the csv data and enter with the createEntry function
for ii in range(len(data)):
    time.sleep(1)
    createEntry(ii)
