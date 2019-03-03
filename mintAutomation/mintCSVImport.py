import pyautogui
import pandas as pd
import time

# Set up auto GUI
pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True

# Button locations
newTransaction = (540, 430)
date = (425, 460)
description = (545, 460)
category = (780, 460)
amount = (910, 460)
notes = (500, 640)
done = (900, 720)

# Read in CSV data
data = pd.read_csv('data.csv', header = 0)
print(data)

print("Load webpage at full size. You have 10 seconds")

for ii in range(5):
    print('.', end='', flush=True)
    time.sleep(2)
#
for ii in range(1):
      pyautogui.click(newTransaction, duration=0.25)

      pyautogui.click(date, duration=0.25)
      pyautogui.hotkey('command', 'a')
      pyautogui.press('delete')
      pyautogui.typewrite(data.iat[0,0])

      pyautogui.click(description, duration=0.25)
      pyautogui.typewrite(data.iat[0,1])

      pyautogui.click(category, duration=0.25)
      pyautogui.typewrite(data.iat[0,2])

      pyautogui.click(amount, duration=0.25)
      pyautogui.typewrite(str(data.iat[0,3]))

      pyautogui.click(notes, duration=0.25)
      pyautogui.typewrite("Imported on ?? from script")

      pyautogui.click(done, duration=0.25)
