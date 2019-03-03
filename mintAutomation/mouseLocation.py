#! python3
import pyautogui, sys

width, height = pyautogui.size()

print("Detected window size: ")
print("Width:" +str(width))
print("Height:" +str(height))
print()
print('Press Ctrl-C to quit.')

try:
    while True:
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
except KeyboardInterrupt:
    print('\n')
