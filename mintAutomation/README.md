# Mint CSV Automation
Mint is a great online finance/budget planner but lacks a .csv import option. The following script can be used to speed up importing large amounts of transactions.

# Must be in the form
The CSV file must have the following headers and be in the form of:

| Date        | Merchant Name | Category | Amount |
| ----------- | ------------- | -------- | ------ |
| 02/27/2019  | Amazon        | Shopping | 30.25  |
| 02/27/2019  | iTunes        | Music    | 5.24   |
| ...         | ...           | ...      | ...    |

## Requirments
Built with Python 3 and the following:
* pyobjc-framework-Quartz
* pyobjc-core
* pyobjc
* PyAutoGUI
* pandas

## Use
1. Use `mouseLocation.py` to find the location of the New Transaction, Date, Notes, and Complete fields in Mint and place the (x,y) values into `mintCSVImport.py`.
2. Run `mintCSVImport.py` and follow the prompts.
Note: You may want to do the first one manually and uncheck "automatically deduct this from my last ATM withdrawal" depending on how you would like to track your data. Mint will remember your saved settings.

## Trouble Shooting
* Website not loading fast enough: Increase `pyautogui.PAUSE` value
