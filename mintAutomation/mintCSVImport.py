import pyautogui
import pandas as pd
import time

# Set up auto GUI
#pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True

# Button locations
newTransaction = (540, 430)
date = (425, 460)
description = (545, 460)
category = (780, 460)
amount = (910, 460)
notes = (500, 660)
done = (900, 760)
checkBox = (470, 570)

# Read in CSV data
data = pd.read_csv('data.csv', header = 0)
print(data)

print("Load webpage at full size. You have 3 seconds")
for ii in range(3):
    print('.', end='', flush=True)
    time.sleep(1)

for ii in range(1):
      pyautogui.click(newTransaction, duration=0.25)

      pyautogui.click(date)
      pyautogui.hotkey('command', 'a')
      pyautogui.press('delete')
      pyautogui.typewrite(data.iat[0,0])
      pyautogui.press('tab')

      pyautogui.typewrite(data.iat[0,1])
      pyautogui.press('tab')

      pyautogui.typewrite(data.iat[0,2])
      pyautogui.press('tab')

      pyautogui.typewrite(str(data.iat[0,3]))

      pyautogui.click(notes)
      pyautogui.typewrite("Imported on ?? from script")

      pyautogui.click(done)
