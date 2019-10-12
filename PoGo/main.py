import pandas as pd
import numpy as np
import pytesseract
import imutils
import time
import math
import glob
import json
import cv2
import re

class getData:
	def __init__(self):
		self.GRAY = None
		self.BGR = None

		self.specie = None
		self.catchDate = None
		self.location = None

		self.CP = None

		self.ATK = None
		self.DEF = None
		self.STA = None
		self.IV = None

		self.isLucky = None
		self.candyCount = None

		self.FTM = None
		self.CTM1 = None
		self.CTM2 = None

		self.ID = None

		self.BGRlower = np.array([10,10,10])
		self.BGRupper = np.array([128,128,128])

	def loadImage(self, filePath):
		# Read in BGR image
		self.BGR = cv2.imread(filePath)

		# Convert to gray color space
		self.GRAY = cv2.cvtColor(self.BGR, cv2.COLOR_BGR2GRAY)

	def showImage(self):
		# Display image
		cv2.imshow('BGR', self.BGR)
		cv2.imshow('GRAY', self.GRAY)

		# Press key (q) to close
		k = cv2.waitKey(0) & 0xFF
		if k == ord('q'):
			cv2.destroyAllWindows()

	def getID(self):
		# img[y1:y2, x1:x2]
		ROI = self.GRAY[900:1010, 275:850]

		# Threshold and invert the image
		_, ROI = cv2.threshold(ROI, 200, 255, cv2.THRESH_BINARY)

		# OCR the name
		self.ID = str(pytesseract.image_to_string(ROI, lang='eng',
			config='--psm 7 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')) \
			+ str(self.CP)

	def getSpecieDateLocation(self):
		# img[y1:y2, x1:x2]
		ROI = self.GRAY[2200:2400, 45:1080]

		# OCR the block of text
		sentance = pytesseract.image_to_string(ROI).split()

		# Split out the sentance to extract components
		self.specie = sentance[1]
		self.catchDate = sentance[5]

		loc = sentance[(sentance.index("around")+1):len(sentance)]
		temp = ''
		for word in loc:
			temp += word

		self.location = temp[0:-1]

	def getCP(self):
		# img[y1:y2, x1:x2]
		ROI = self.GRAY[120:230, 340:730]

		# Remove background by thresholding
		_, ROI = cv2.threshold(ROI, 250, 255, cv2.THRESH_BINARY)

		# Bold the letters for easier OCR
		kernel = np.ones((2,2),np.uint8)
		ROI = cv2.dilate(ROI, kernel, iterations = 3)

		# Invert image for better OCR
		ROI = cv2.bitwise_not(ROI)

		# OCR the value
		self.CP = pytesseract.image_to_string(ROI, lang='eng',
			config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789')

	def getStats(self):
		# Cropping coordinates
		x1 = 130
		x2 = 530
		top = [1850, 1960, 2070]
		bottom = [1910, 2020, 2130]

		# Storage variable
		stats = []

		# Loop for each stat
		for ii in range(3):
			# img[y1:y2, x1:x2]
			ROI = self.GRAY[top[ii]:bottom[ii], x1:x2]

			# Threshold and invert the image
			_, ROI = cv2.threshold(ROI, 200, 255, cv2.THRESH_BINARY)
			ROI = cv2.bitwise_not(ROI)

			# cv2.RETR_EXTERNAL: Only extreme outer flags. All child contours are left behind.
			# CHAIN_APPROX_SIMPLE: Removes all redundant points and compresses the contour.
			region = cv2.findContours(ROI, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			region = imutils.grab_contours(region)

			# Initialize value for the number of pixels highlighted
			widthSum = 0
			for reg in region:
				# Add the pixel space between bars
				if widthSum > 0:
					widthSum += 5

				# Add the number of pixels highlighted in a region
				_,_,w,_ = cv2.boundingRect(reg)
				widthSum += w

			# Interpolate the percentage of the bar between 0 and 15 and append to storage
			statVal = np.interp((widthSum/370), list(np.linspace(0,1,16)), list(range(0,16)))
			stats.append(round(statVal))

		# Extract and save the data
		self.ATK = int(stats[0])
		self.DEF = int(stats[1])
		self.STA = int(stats[2])
		self.IV = int(round((sum(stats) / 45) * 100))

	def getLuckyCandy(self):
		# img[y1:y2, x1:x2] -> Lucky?
		ROI = self.GRAY[1000:1070, 300:800]

		# Check string for lucky
		str = pytesseract.image_to_string(ROI).split()

		# Change crop area based on luck
		if str[0] == 'LUCKY':
			# True path
			self.isLucky = True

			# img[y1:y2, x1:x2] -> Candy
			ROI = self.BGR[1450:1520, 745:845]
			ROI = cv2.inRange(ROI, self.BGRlower, self.BGRupper)

			# Invert image for better OCR
			ROI = cv2.bitwise_not(ROI)

			self.candyCount = pytesseract.image_to_string(ROI,
				config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789')
		else:
			# False path
			self.isLucky = False

			# img[y1:y2, x1:x2] -> Candy
			ROI = self.BGR[1400:1460, 745:845]
			ROI = cv2.inRange(ROI, self.BGRlower, self.BGRupper)

			# Invert image for better OCR
			ROI = cv2.bitwise_not(ROI)

			self.candyCount = pytesseract.image_to_string(ROI,
				config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789')

	def getMoves(self):
		# img[y1:y2, x1:x2]
		ROI = self.BGR[1890:2360, 145:600]

		# Threshold image
		ROI = cv2.inRange(ROI, self.BGRlower, self.BGRupper)

		# Erode and dialte the image to get rid of unwanted pixels
		kernel = np.ones((2,2),np.uint8)
		ROI = cv2.erode(ROI, kernel, iterations = 2)
		ROI = cv2.dilate(ROI, kernel, iterations = 2)

		# cv2.RETR_EXTERNAL: Only extreme outer flags. All child contours are left behind.
		# CHAIN_APPROX_SIMPLE: Removes all redundant points and compresses the contour.
		region = cv2.findContours(ROI, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		region = imutils.grab_contours(region)

		# Remove anything thats not a word
		for reg in region:
			if cv2.contourArea(reg) > 1000:
				cv2.drawContours(ROI, [reg], -1, 0, -1)

		# Invert the image
		ROI = cv2.bitwise_not(ROI)

		# Read the text
		moves = pytesseract.image_to_string(ROI).split("\n")

		# Remove empty strings
		moves = list(filter(None, moves))

		# Assign moves to variables
		if len(moves) is 3:
			self.FTM = moves[0].replace('-',' ')
			self.CTM1 = moves[1].replace('-',' ')
			self.CTM2 = moves[2].replace('-',' ')
		elif len(moves) is 2:
			self.FTM = moves[0].replace('-',' ')
			self.CTM1 = moves[1].replace('-',' ')

	def resetVariables(self):
		# Reset variables to None so errors can be regonized
		self.GRAY = None
		self.BGR = None

		self.specie = None
		self.catchDate = None
		self.location = None

		self.CP = None

		self.ATK = None
		self.DEF = None
		self.STA = None
		self.IV = None

		self.isLucky = None
		self.candyCount = None

		self.FTM = None
		self.CTM1 = None
		self.CTM2 = None

		self.ID = None

	def logDataA(self, fileName, printFlag, csvFlag):
		# Storage variable
		tempData = []

		# Load all *.PNG files in dataA directory
		for filePath in glob.iglob('dataA/*.PNG'):
			# Load image
			self.loadImage(filePath)

			# Get the data
			self.getLuckyCandy()
			self.getCP()
			self.getID()
			self.getMoves()

			# Print
			if printFlag is True:
				print('ID:\t', self.ID)
				print(self.isLucky, self.candyCount)
				print(self.FTM, self.CTM1, self.CTM2)

			# Save the data to temp list and reset
			tempData.append([self.ID, self.isLucky, self.candyCount, self.FTM,
							 self.CTM1, self.CTM2])
			self.resetVariables()

		# Write data to CSV and display to user
		if csvFlag is True:
			df = pd.DataFrame(tempData, columns=['ID', 'Lucky', 'Candy Count',
				'Fast Attack', 'Charge Attack 1', 'Charge Attack 2'])

			df.to_csv(fileName, index=None, header=True)
			print('\nFile saved to:\t' + fileName + '\n\n\n')

	def logDataB(self, fileName, printFlag, csvFlag):
		# Storage variable
		tempData = []

		# Load all *.PNG files in dataB directory
		for filePath in glob.iglob('dataB/*.PNG'):
			# Load image
			self.loadImage(filePath)

			# Get the data
			self.getSpecieDateLocation()
			self.getCP()
			self.getID()
			self.getStats()

			# Print
			if printFlag is True:
				print('ID:\t', self.ID)
				print(self.specie, self.CP)
				print(self.ATK, self.DEF, self.STA, '->', self.IV)
				print(self.catchDate, self.location, '\n')

			# Save the data to temp list and reset
			tempData.append([self.ID, self.specie, self.CP, self.ATK, self.DEF,
							 self.STA, self.IV, self.catchDate, self.location])
			self.resetVariables()

		# Write data to CSV and display to user
		if csvFlag is True:
			df = pd.DataFrame(tempData, columns=['ID', 'Specie', 'CP', 'ATK_IV',
				'DEF_IV', 'STA_IV', 'Percent IV', 'Catch Date', 'Catch Location'])

			df.to_csv(fileName, index=None, header=True)
			print('\nFile saved to:\t' + fileName + '\n\n\n')

class calculateData:
	def __init__(self):
		self.MASTER = None

		self.gameData = None
		self.moveData = None

		self.CPM = [0.094, 0.135137432, 0.16639787, 0.192650919, 0.21573247, 0.236572661, 0.25572005,
				   0.273530381, 0.29024988, 0.306057378, 0.3210876, 0.335445036, 0.34921268, 0.362457751,
				   0.3752356, 0.387592416, 0.39956728, 0.411193551, 0.4225, 0.432926409, 0.44310755,
				   0.453059959, 0.4627984, 0.472336093, 0.48168495, 0.4908558, 0.49985844, 0.508701765,
				   0.51739395, 0.525942511, 0.5343543, 0.542635738, 0.5507927, 0.558830586, 0.5667545,
				   0.574569133, 0.5822789, 0.589887907, 0.5974, 0.604823665, 0.6121573, 0.619404122,
				   0.6265671, 0.633649143, 0.64065295, 0.647580967, 0.65443563, 0.661219252, 0.667934,
				   0.674581896, 0.6811649, 0.687684904, 0.69414365, 0.70054287, 0.7068842, 0.713169109,
				   0.7193991, 0.725575614, 0.7317, 0.734741009, 0.7377695, 0.740785594, 0.74378943,
				   0.746781211, 0.74976104, 0.752729087, 0.7556855, 0.758630368, 0.76156384, 0.764486065,
				   0.76739717, 0.770297266, 0.7731865, 0.776064962, 0.77893275, 0.781790055, 0.784637,
				   0.787473608, 0.7903]

	def loadImgData(self, fileA, fileB):
		# Load the 2 CSV files and index by ID
		A = pd.read_csv(fileA, header = 0, names = ['ID', 'Lucky', 'Candy Count',
			'Fast Attack', 'Charge Attack 1', 'Charge Attack 2'], index_col='ID')

		B = pd.read_csv(fileB, header = 0, names = ['ID', 'Specie', 'CP', 'ATK_IV',
			'DEF_IV', 'STA_IV', 'Percent IV', 'Catch Date', 'Catch Location'], index_col='ID')

		# Merge into single data frame
		self.MASTER = B.merge(A, how='outer', left_index=True, right_index=True)

	def loadJsonData(self, gameMasterFile):
		# Load in the GAME_MASTER file
		with open(gameMasterFile) as jsonFile:
			data = json.load(jsonFile)

		# Regex to match V####_POKEMON_
		patternA = re.compile('^V\d{4}_POKEMON_.*$')
		patternB = re.compile('^V\d{4}_MOVE_.*$')

		# List for storage
		pokemonGameData = []
		pokemonMoveData = []

		for template in data['itemTemplates']:
			# Pokemon info
			if patternA.match(template['templateId']):
				# Make a dictionary row
				dictRow = {}

				# Pokemon Template ID
				dictRow['TemplateId'] = template['templateId']

				# Pokemon Number
				pokemonNumber = re.findall("\d{4}", template['templateId'])
				pokemonNumber = int(pokemonNumber[0])
				dictRow['Number'] = pokemonNumber

				# Pokemon Name
				name = template['pokemonSettings']['pokemonId']
				dictRow['Name'] = name

				# Pokemon form and remove name
				form = template['pokemonSettings'].get('form', '')
				form = form.replace(name+'_', '').replace('_',' ')
				dictRow['Form'] = form

				# Stats
				dictRow['baseStamina'] = template['pokemonSettings']['stats']['baseStamina']
				dictRow['baseAttack'] = template['pokemonSettings']['stats']['baseAttack']
				dictRow['baseDefense'] = template['pokemonSettings']['stats']['baseDefense']

				# Walking distance and evolution cost
				dictRow['kmBuddyDistance'] = int(template['pokemonSettings'].get('kmBuddyDistance', 0.0))
				try:
					dictRow['candyCost'] = int(template['pokemonSettings'].get('candyToEvolve', 0.0))
				except:
					dictRow['candyCost'] = -1

				# Get type
				try:
					type = template['pokemonSettings'].get('type', '')
					type = type.replace('POKEMON_TYPE_','')
					dictRow['type'] = type

					type2 = template['pokemonSettings'].get('type2', '')
					type2 = type2.replace('POKEMON_TYPE_','')
					dictRow['type2'] = type2
				except:
					pokemonType = template['pokemonSettings'].get('pokemonType', '')
					pokemonType = pokemonType.replace('POKEMON_TYPE_','')
					dictRow['pokemonType'] = pokemonType

				#if form != 'NORMAL': # ignore NORMAL forms because they are duplicates
				pokemonGameData.append(dictRow)

			# Moveset info
			if patternB.match(template['templateId']):
				# Make a dictionary row
				dictRow = {}

				# Pokemon Template ID
				dictRow['TemplateId'] = template['templateId']

				# movementId
				movementId = template['moveSettings']['movementId']
				movementId = movementId.replace('_', ' ')
				movementId = movementId.replace(' FAST','')
				dictRow['movementId'] = movementId

				# Power
				dictRow['power'] = int(template['moveSettings'].get('power', 0.0))

				# Type
				pokemonType = template['moveSettings']['pokemonType']
				pokemonType = pokemonType.replace('POKEMON_TYPE_','')
				dictRow['pokemonType'] = pokemonType

				# Log the data
				pokemonMoveData.append(dictRow)

		self.gameData = pd.DataFrame(pokemonGameData)
		self.moveData = pd.DataFrame(pokemonMoveData)

	def halfRound(self, num):
		return round(num * 2.0) / 2.0

	def calcLevelAndBaseStats(self):
		# Create list for writing
		levelList = []
		atkBaseList = []
		defBaseList = []
		staBaseList = []

		for ii in range(self.MASTER.shape[0]):
			# Get value from json
			str = self.MASTER['Specie'][ii]
			row = self.gameData.index[self.gameData['Name'] == str.upper()][0]

			Base_Attack = self.gameData['baseAttack'][row]
			Base_Defense = self.gameData['baseDefense'][row]
			Base_Stamina = self.gameData['baseStamina'][row]

			# Find CP multiplier
			CP_Multiplier = math.sqrt((10 * self.MASTER['CP'][ii]) /
							((Base_Attack + self.MASTER['ATK_IV'][ii]) *
							(Base_Defense + self.MASTER['DEF_IV'][ii])**0.5 *
							(Base_Stamina + self.MASTER['STA_IV'][ii])**0.5))

			# Reverse CP multiplier to find level
			levelList.append(self.halfRound(np.interp(CP_Multiplier, self.CPM,
							 np.arange(1, 40.5, 0.5).tolist())))

			# Append lists for base stats
			atkBaseList.append(Base_Attack)
			defBaseList.append(Base_Defense)
			staBaseList.append(Base_Stamina)

		# Add to data frame
		self.MASTER['Level'] = levelList
		self.MASTER['ATK_Base'] = atkBaseList
		self.MASTER['DEF_Base'] = defBaseList
		self.MASTER['STA_Base'] = staBaseList

	def numberTypeCandy(self):
		# Create list for writing
		pokedexNum = []
		type = []
		type2 = []
		walkDistance = []
		evolutionCost = []

		for ii in range(self.MASTER.shape[0]):
			# Get index from json using name
			str = self.MASTER['Specie'][ii]
			row = self.gameData.index[self.gameData['Name'] == str.upper()][0]

			# Append data to a list
			pokedexNum.append(self.gameData['Number'][row])
			type.append(self.gameData['type'][row])
			type2.append(self.gameData['type2'][row])
			walkDistance.append(self.gameData['kmBuddyDistance'][row])
			evolutionCost.append(self.gameData['candyCost'][row])

		# save to dataframe
		self.MASTER['Pokedex Number'] = pokedexNum
		self.MASTER['type'] = type
		self.MASTER['type2'] = type2
		self.MASTER['Walking Distance'] = walkDistance
		self.MASTER['Evolution Cost'] = evolutionCost

	def moves(self):
		# Create lists for writing
		fastType = []
		fastPwr = []
		chrgType = []
		chrgPwr = []

		for ii in range(self.MASTER.shape[0]):
			# Get index from json using attack
			str = self.MASTER['Fast Attack'][ii]
			row = self.moveData.index[self.moveData['movementId'] == str.upper()][0]
			fastType.append(self.moveData['pokemonType'][row])
			fastPwr.append(self.moveData['power'][row])

			str = self.MASTER['Charge Attack 1'][ii]
			row = self.moveData.index[self.moveData['movementId'] == str.upper()][0]
			chrgType.append(self.moveData['pokemonType'][row])
			chrgPwr.append(self.moveData['power'][row])

		self.MASTER['Fast Attack Type'] = fastType
		self.MASTER['Fast Attack Power'] = fastPwr
		self.MASTER['Charge Attack Type'] = chrgType
		self.MASTER['Charge Attack Power'] = chrgPwr

	def exportData(self, fileA, fileB, JSON, fileName):
		# Run all the processing
		self.loadImgData(fileA, fileB)
		self.loadJsonData(JSON)
		self.calcLevelAndBaseStats()
		self.numberTypeCandy()
		self.moves()

		# Rearrange columns
		self.MASTER = self.MASTER[['Pokedex Number', 'Specie', 'CP', 'type',
			'type2', 'ATK_IV', 'DEF_IV', 'STA_IV', 'Percent IV',
			'ATK_Base', 'DEF_Base', 'STA_Base', 'Level',
			'Fast Attack', 'Fast Attack Type', 'Fast Attack Power',
			'Charge Attack 1', 'Charge Attack Type', 'Charge Attack Power',
			'Charge Attack 2', 'Walking Distance', 'Candy Count', 'Evolution Cost',
			'Lucky', 'Catch Date', 'Catch Location']]

		# Save to file
		self.MASTER.to_csv(fileName)
		print('\nFile saved to:\t' + fileName + '\n')

def main():
	G = getData()
	C = calculateData()

	# Start time
	startTime = time.time()

	# Log data -> Filename, printFlag, csvFlag
	G.logDataA('dataA.csv', True, True)
	G.logDataB('dataB.csv', True, True)

	# Load data -> FileA, FileB, gameMasterFile, file2save
	C.exportData('dataA.csv', 'dataB.csv', 'GAME_MASTER.json', 'MASTER.csv')

	# Time elapsed
	print('Time elapsed: ', time.time() - startTime)

# Main loop
if __name__ == '__main__':
	main()
