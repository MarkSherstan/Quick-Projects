# PoGo
Playing around with OpenCV, tesseract, and JSON files to make a spreadsheet for Pokemon Go.

## Comments
Learned how to parse JSONs and relearned a lot about OpenCV and OCR. The project may be further optimized in the future for all proper error handling, region identification, program generalization, etc... If someone is actually going to use this I would recommend loading just the image data and manually inspecting the .csv before running the calculations and data acquisition from the json.   

## Requirements
Software requirements and install steps for MacOS.

```
brew install tesseract --HEAD


pip3 install pytesseract
pip3 install opencv-python
pip3 install imutils
```

## Use
Photos must be 1125 × 2436 and `*.PNG` format.

1. Upload IV screenshot to a folder caled `screenShots`
2. Retrieve the most up to date GAME_MASTER.json file in your command line with: `wget https://raw.githubusercontent.com/pokemongo-dev-contrib/pokemongo-game-master/master/versions/latest/GAME_MASTER.json`
3. Run `main.py` and edit lines accordingly
```
	# Ensure images are in 'screenShots' folder. Specify file name
	G.loadImageData('imgData.csv')

	# Load saved file imageData.csv, gameMasterFile.json and specify new file name file2save.csv
	P.exportData('imgData.csv', 'GAME_MASTER.json', 'MASTER.csv')
```

Look at the `exampleData` folder for more information.

## To do
* Clean up the spaghetti -> Make some nicer sub functions (e.g. - send ROI and return string)
* Add arguments in command line vs hardcoded (argparse) -> fileNames
* Look at json parsing, OCR, and image processing in Swift

## Links
Helpful links and helpful code:
* https://github.com/tesseract-ocr/tesseract/blob/master/doc/tesseract.1.asc
* https://github.com/slyt/Pokemon-Go-CP-Plots
* http://taylorsly.com/plotting-pokemon-max-combat-power/
