import pyautogui
import pandas as pd
import time
import datetime

# Get current time stamp
now = datetime.datetime.now()
timeStamp = now.strftime("%Y-%m-%d")

# Set up auto GUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.15

# Button locations
newTransaction = (528, 458)
date = (405, 530)
notes = (500, 725)
done = (900, 790)

# Read in CSV data
data = pd.read_csv('data.csv', header = 0)

# Give time for user to navigate to page
print("Load webpage on left side of screen and terminal on right hand side. You have 2 seconds")
for ii in range(2):
    print('.', end='', flush=True)
    time.sleep(1)

# Function for entering data
def createEntry(idx):
     pyautogui.click(newTransaction)

     pyautogui.click(date)
     pyautogui.hotkey('ctrl', 'a')

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

     pyautogui.click((1520, 426))
     time.sleep(0.5)

# Loop through all the csv data and enter with the createEntry function
for ii in range(len(data)):
    createEntry(ii)
    print(str(data.iat[ii,0]) + '\t' + str(data.iat[ii,1]) + '\t' + str(data.iat[ii,2]) + '\t' + str(data.iat[ii,3]))
    x = input()
