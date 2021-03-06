import pandas as pd
import numpy as np
import pytesseract
import imutils
import math
import glob
import json
import cv2
import re

class getImgData:
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

		self.BGRlower = np.array([10,10,10])
		self.BGRupper = np.array([128,128,128])

	def loadImage(self, fileName):
		# Read in BGR image
		self.BGR = cv2.imread(fileName)

		# Convert to gray color space
		self.GRAY = cv2.cvtColor(self.BGR, cv2.COLOR_BGR2GRAY)

	def getSpecieDateLocation(self):
		# img[y1:y2, x1:x2]
		ROI = self.GRAY[2100:2400, 45:1080]

		# OCR the block of text
		sentance = pytesseract.image_to_string(ROI).split()

		# Split out the sentance to extract components
		spec = sentance[1:(sentance.index("was"))]
		temp = ''
		for word in spec:
			temp += word
		self.specie = temp.replace("'", "").replace('.','_')

		self.catchDate = ''.join(sentance[(sentance.index("on")+1):(sentance.index("on")+2)])

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

		# Error case for CP
		try:
			# Convert CP to int
			self.CP = int(self.CP)

			# If CP is impossibly high or low, get input from user
			if not (2000 <= self.CP <= 4000):
				cv2.imshow('ERROR', self.BGR[120:230, 340:730])
				cv2.waitKey(1000)
				self.CP = int(input("Input CP: "))

				# Fix black screen bug
				for ii in range (1,10):
					cv2.destroyAllWindows()
					cv2.waitKey(10)

		except:
			# If int conversion went wrong get input from user
			cv2.imshow('ERROR', self.BGR[120:230, 340:730])
			cv2.waitKey(1000)
			self.CP = int(input("Input CP: "))

			# Fix black screen bug
			for ii in range (1,10):
				cv2.destroyAllWindows()
				cv2.waitKey(10)

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

	def luck(self):
		# img[y1:y2, x1:x2]
		ROI = self.GRAY[1000:1070, 300:800]

		# Check string for lucky
		str = pytesseract.image_to_string(ROI).split()

		if str[0] == 'LUCKY':
			self.isLucky = True
		else:
			self.isLucky = False

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

	def loadImageData(self, fileName):
		# Storage variable
		tempData = []
		errorList = []

		# Load all *.PNG files in specified directory
		for filePath in glob.iglob('screenShots/*.PNG'):
			# Load image
			self.loadImage(filePath)

			# Get the data
			try:
				self.getSpecieDateLocation()
				self.getCP()
				self.luck()
				self.getStats()
			except:
				self.resetVariables()
				errorList.append(filePath)

			# Print
			print(self.specie, self.CP)
			print(self.ATK, self.DEF, self.STA, '->', self.IV)
			print(self.catchDate, self.location, self.isLucky, '\n')

			# Save the data to temp list and reset
			tempData.append([self.specie, self.CP, self.ATK, self.DEF, self.STA,
							 self.IV, self.catchDate, self.location, self.isLucky])
			self.resetVariables()

		# Write data to CSV and display file name to user
		df = pd.DataFrame(tempData, columns=['Specie', 'CP', 'ATK_IV', 'DEF_IV',
											 'STA_IV', 'Percent IV', 'Catch Date',
											 'Catch Location', 'Lucky'])

		df.to_csv(fileName, index=None, header=True)
		print('\n\n\n\nFile saved to:\t' + fileName)
		print('Errors in file: ', errorList)

class processData:
	def __init__(self):
		self.MASTER = None
		self.gameData = None

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

	def loadImgData(self, fileName):
		# Load the 2 CSV files and index by ID
		self.MASTER = pd.read_csv(fileName, header = 0,
								  names = ['Specie', 'CP', 'ATK_IV', 'DEF_IV',
										   'STA_IV', 'Percent IV', 'Catch Date',
										   'Catch Location', 'Lucky'])

	def loadJsonData(self, gameMasterFile):
		# Load in the GAME_MASTER file
		with open(gameMasterFile) as jsonFile:
			data = json.load(jsonFile)

		# Regex to match V####_POKEMON_
		patternA = re.compile('^V\d{4}_POKEMON_.*$')

		# List for storage
		pokemonGameData = []

		for template in data['itemTemplates']:
			# Pokemon info
			if patternA.match(template['templateId']):
				# Make a dictionary row
				dictRow = {}

				# Pokemon number
				pokemonNumber = re.findall("\d{4}", template['templateId'])
				pokemonNumber = int(pokemonNumber[0])
				dictRow['Number'] = pokemonNumber

				# Pokemon name
				name = template['pokemonSettings']['pokemonId']
				dictRow['Name'] = name

				# Pokemon form and remove name
				form = template['pokemonSettings'].get('form', '')
				form = form.replace(name+'_', '').replace('_',' ')

				# Base stats
				dictRow['baseStamina'] = template['pokemonSettings']['stats']['baseStamina']
				dictRow['baseAttack'] = template['pokemonSettings']['stats']['baseAttack']
				dictRow['baseDefense'] = template['pokemonSettings']['stats']['baseDefense']

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

				# Only log blank forms as with current data anything else is duplicates
				if form is '':
					pokemonGameData.append(dictRow)

		# Save to a data frame
		self.gameData = pd.DataFrame(pokemonGameData)

	def halfRound(self, num):
		return round(num * 2.0) / 2.0

	def levelAndBaseStats(self):
		# Create list for writing
		levelList = []
		CPMList = []
		atkBaseList = []
		defBaseList = []
		staBaseList = []

		try:
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
				CPMList.append(round(CP_Multiplier, 5))

				# Append lists for base stats
				atkBaseList.append(Base_Attack)
				defBaseList.append(Base_Defense)
				staBaseList.append(Base_Stamina)
		except:
			print(self.MASTER['Specie'][ii])

		# Add to data frame
		self.MASTER['Level'] = levelList
		self.MASTER['CPM'] = CPMList
		self.MASTER['ATK_Base'] = atkBaseList
		self.MASTER['DEF_Base'] = defBaseList
		self.MASTER['STA_Base'] = staBaseList

	def numberAndTypes(self):
		# Create list for writing
		pokedexNum = []
		type = []
		type2 = []

		for ii in range(self.MASTER.shape[0]):
			# Get index from json using name
			str = self.MASTER['Specie'][ii]
			row = self.gameData.index[self.gameData['Name'] == str.upper()][0]

			# Append data to a list
			pokedexNum.append(self.gameData['Number'][row])
			type.append(self.gameData['type'][row])
			type2.append(self.gameData['type2'][row])

		# save to dataframe
		self.MASTER['Pokedex Number'] = pokedexNum
		self.MASTER['typeA'] = type
		self.MASTER['typeB'] = type2
		self.MASTER['types'] = self.MASTER['typeA']+'-'+self.MASTER['typeB']

	def comparisonData(self):
		# Level 40 perfect IV CP value
		self.MASTER['Perfect CP'] = (round(((self.MASTER.ATK_Base + 15) *
									 	(self.MASTER.DEF_Base + 15)**0.5 *
									 	(self.MASTER.STA_Base + 15)**0.5 *
									 	(0.7903)**2) / 10)).astype('Int64')

		# Current ATK, DEF, HP based on level
		self.MASTER['ATK_Current'] = (round((self.MASTER.ATK_Base + self.MASTER.ATK_IV) * self.MASTER.CPM)).astype('Int64')
		self.MASTER['DEF_Current'] = (round((self.MASTER.DEF_Base + self.MASTER.DEF_IV) * self.MASTER.CPM)).astype('Int64')
		self.MASTER['STA_Current'] = (round((self.MASTER.STA_Base + self.MASTER.STA_IV) * self.MASTER.CPM)).astype('Int64')

	def exportData(self, imgDataFilePath, JSON, exportFilePath):
		# Run all the processing
		self.loadImgData(imgDataFilePath)
		self.loadJsonData(JSON)
		self.levelAndBaseStats()
		self.numberAndTypes()
		self.comparisonData()

		# Rearrange columns
		self.MASTER = self.MASTER[['Pokedex Number', 'Specie', 'CP', 'typeA', 'typeB',
			'types', 'ATK_IV', 'DEF_IV', 'STA_IV', 'Percent IV', 'Level', 'CPM', 'Perfect CP',
			'ATK_Current', 'DEF_Current', 'STA_Current',
			'ATK_Base', 'DEF_Base', 'STA_Base',
			'Lucky', 'Catch Date', 'Catch Location']]

		# Save to file
		self.MASTER.to_csv(exportFilePath)
		print('\nFile saved to:\t' + exportFilePath + '\n')

class selector:
	def __init__(self):
		self.gameData = None
		self.moveData = None
		self.userData = None

		data = np.array([
		['Atk-Def', 'NORMAL','FIGHTING','FLYING','POISON','GROUND','ROCK','BUG','GHOST','STEEL','FIRE','WATER','GRASS','ELECTRIC','PSYCHIC','ICE','DRAGON','DARK','FAIRY'],
		['NORMAL',1,1,1,1,1,0.625,1,0.391,0.625,1,1,1,1,1,1,1,1,1],
		['FIGHTING',1.6,1,0.625,0.625,1,1.6,0.625,0.391,1.6,1,1,1,1,0.625,1.6,1,1.6,0.625],
		['FLYING',1,1.6,1,1,1,0.625,1.6,1,0.625,1,1,1.6,0.625,1,1,1,1,1],
		['POISON',1,1,1,0.625,0.625,0.625,1,0.625,0.391,1,1,1.6,1,1,1,1,1,1.6],
		['GROUND',1,1,0.391,1.6,1,1.6,0.625,1,1.6,1.6,1,0.625,1.6,1,1,1,1,1],
		['ROCK',1,0.625,1.6,1,0.625,1,1.6,1,0.625,1.6,1,1,1,1,1.6,1,1,1],
		['BUG',1,0.625,0.625,0.625,1,1,1,0.625,0.625,0.625,1,1.6,1,1.6,1,1,1.6,0.625],
		['GHOST',0.391,1,1,1,1,1,1,1.6,1,1,1,1,1,1.6,1,1,0.625,1],
		['STEEL',1,1,1,1,1,1.6,1,1,0.625,0.625,0.625,1,0.625,1,1.6,1,1,1.6],
		['FIRE',1,1,1,1,1,0.625,1.6,1,1.6,0.625,0.625,1.6,1,1,1.6,0.625,1,1],
		['WATER',1,1,1,1,1.6,1.6,1,1,1,1.6,0.625,0.625,1,1,1,0.625,1,1],
		['GRASS',1,1,0.625,0.625,1.6,1.6,0.625,1,0.625,0.625,1.6,0.625,1,1,1,0.625,1,1],
		['ELECTRIC',1,1,1.6,1,0.391,1,1,1,1,1,1.6,0.625,0.625,1,1,0.625,1,1],
		['PSYCHIC',1,1.6,1,1.6,1,1,1,1,0.625,1,1,1,1,0.625,1,1,0.391,1],
		['ICE',1,1,1.6,1,1.6,1,1,1,0.625,0.625,0.625,1.6,1,1,0.625,1.6,1,1],
		['DRAGON',1,1,1,1,1,1,1,1,0.625,1,1,1,1,1,1,1.6,1,0.391],
		['DARK',1,0.625,1,1,1,1,1,1.6,1,1,1,1,1,1.6,1,1,0.625,0.625],
		['FAIRY',1,1.6,1,0.625,1,1,1,1,0.625,0.625,1,1,1,1,1,1.6,1.6,1]])

		self.typeChart = pd.DataFrame(data=data[1:,1:],    # values
								 index=data[1:,0],    	   # 1st column as index
							  	 columns=data[0,1:])       # 1st row as the column names

	def loadPokemonData(self, gameMasterFile):
		# Load in the GAME_MASTER file
		with open(gameMasterFile) as jsonFile:
			data = json.load(jsonFile)

		# Regex to match V####_POKEMON_
		patternA = re.compile('^V\d{4}_POKEMON_.*$')

		# List for storage
		pokemonGameData = []

		for template in data['itemTemplates']:
			# Pokemon info
			if patternA.match(template['templateId']):
				# Make a dictionary row
				dictRow = {}

				# Pokemon number
				pokemonNumber = re.findall("\d{4}", template['templateId'])
				pokemonNumber = int(pokemonNumber[0])
				dictRow['Number'] = pokemonNumber

				# Pokemon name
				name = template['pokemonSettings']['pokemonId']
				dictRow['Name'] = name

				# Quick Moves
				try:
					quickMoves = template['pokemonSettings']['quickMoves']
					dictRow['quickMoves'] = quickMoves
				except:
					continue

				# Charge moves
				try:
					chargeMoves = template['pokemonSettings']['cinematicMoves']
					dictRow['chargeMoves'] = chargeMoves
				except:
					continue

				# Form
				form = template['pokemonSettings'].get('form', '')
				form = form.replace(name+'_', '').replace('_',' ')
				dictRow['form'] = form

				# Only log blank forms as with current data anything else is duplicates
				if form is '':
					pokemonGameData.append(dictRow)

		# Save to a data frame
		self.gameData = pd.DataFrame(pokemonGameData)
		# print(self.gameData.head(7))

	def loadMoveData(self, gameMasterFile):
		# Load in the GAME_MASTER file
		with open(gameMasterFile) as jsonFile:
			data = json.load(jsonFile)

		# Regex to match V####_MOVE_
		patternA = re.compile('^V\d{4}_MOVE_.*$')

		# List for storage
		pokemonGameData = []

		for template in data['itemTemplates']:
			# Pokemon info
			if patternA.match(template['templateId']):
				# Make a dictionary row
				dictRow = {}

				# Move ID
				uniqueID = template['moveSettings']['movementId']
				dictRow['uniqueID'] = uniqueID

				# Type
				type = template['moveSettings']['pokemonType']
				type = type.replace('POKEMON_TYPE_', '')
				dictRow['type'] = type

				# Duration
				duration = template['moveSettings']['durationMs'] / 1000
				dictRow['duration'] = duration

				# DPS
				try:
					power = template['moveSettings']['power']
					dictRow['power'] = power
					# dictRow['DPS'] = power / duration
				except:
					dictRow['power'] = 0
					# dictRow['DPS'] = 0

				# Energy
				try:
					energyDelta = template['moveSettings']['energyDelta']
					dictRow['energyDelta'] = energyDelta

					if energyDelta > 0:
						dictRow['FastMove'] = True
						# dictRow['EPS'] = energyDelta / duration
					else:
						dictRow['FastMove'] = False
						# dictRow['EPS'] = -1
				except:
					dictRow['energyDelta'] = 0
					# dictRow['EPS'] = 0

				# Log the data
				pokemonGameData.append(dictRow)

		# Save to a data frame
		self.moveData = pd.DataFrame(pokemonGameData)
		# print(self.moveData.head(7))

	def loadUserData(self, fileName):
		self.userData = pd.read_csv(fileName)
		# print(self.userData.head(7))

	def typeBonus(self, DPS, moveType, atkTypeA, atkTypeB, defTypeA, defTypeB):
		# Initialize variables
		STAB = 1.0

		# Same type attack bonus
		if ((moveType == atkTypeA) or (moveType == atkTypeB)):
			STAB = 1.2

		# Type bonus [Defender][Attacker]
		typeBonusA = float(self.typeChart[defTypeA][moveType])

		try:
			typeBonusB = float(self.typeChart[defTypeB][moveType])
		except:
			typeBonusB = 1.0

		# Update DPS
		return DPS * STAB * typeBonusA * typeBonusB

	def optimize(self, defTypeA, defTypeB, defDef=200):
		self.userData['Moveset'] = ''
		self.userData['DPS'] = ''

		for ii in range(self.userData.shape[0]):
			# Match up numbers
			num = self.userData['Pokedex Number'][ii]
			atkTypeA = self.userData['typeA'][ii]
			atkTypeB = self.userData['typeB'][ii]
			atkCurrent = self.userData['ATK_Current'][ii]

			row = self.gameData.index[self.gameData['Number'] == num][0]

			quickMoves = self.gameData['quickMoves'][row]
			chargeMoves = self.gameData['chargeMoves'][row]

			# List for storage
			dictList = []

			for qMove in quickMoves:
				# Retrieve some values (quick)
				qIdx = self.moveData.index[self.moveData['uniqueID'] == qMove][0]
				qType = self.moveData['type'][qIdx]
				qPower = self.moveData['power'][qIdx]
				qEnergy = self.moveData['energyDelta'][qIdx]
				qDuration = self.moveData['duration'][qIdx]

				# Update qPower
				qPower = self.typeBonus(qPower, qType, atkTypeA, atkTypeB, defTypeA, defTypeB)
				qNum100 = math.ceil(abs(100.0 / qEnergy))
				qDmg = qPower * qNum100
				qTime = qDuration * qNum100

				for cMove in chargeMoves:
					# Make a dictionary row
					dictRow = {}

					# Store the moves
					dictRow['Name'] = qMove.replace('_',' ').replace('FAST','') + '& ' + cMove.replace('_',' ')

					# Retrieve some values (charged)
					cIdx = self.moveData.index[self.moveData['uniqueID'] == cMove][0]
					cEnergy = self.moveData['energyDelta'][cIdx]
					cPower = self.moveData['power'][cIdx]
					cType = self.moveData['type'][cIdx]
					cDuration = self.moveData['duration'][cIdx]

					# Update cPower
					cPower = self.typeBonus(cPower, qType, atkTypeA, atkTypeB, defTypeA, defTypeB)
					cNum100 = math.floor(abs(100.0 / cEnergy))
					cDmg = cPower * cNum100
					cTime = cDuration * cNum100

					# Total DPS
					DPS = (qDmg + cDmg) / (qTime + cTime)
					DPS = atkCurrent/defDef * DPS

					# Store results
					dictRow['DPS'] = DPS
					dictList.append(dictRow)

			# Find the largest value and store in df
			maxDPS = max(dictList, key=lambda x:x['DPS'])
			self.userData['Moveset'][ii] = maxDPS['Name']
			self.userData['DPS'][ii] = maxDPS['DPS']

		# print(self.userData.head(10))
		sortedData = self.userData.sort_values(by=['DPS'], ascending=False)
		print(sortedData.head(20))

def main():
	# Set up classes
	G = getImgData()
	P = processData()
	S = selector()

	# Ensure images are in 'screenShots' folder. Specify file name...
	G.loadImageData('imgData.csv')

	# Load saved file imageData.csv, gameMasterFile.json and specify new file name file2save.csv
	P.exportData('imgData.csv', 'GAME_MASTER.json', 'MASTER.csv')

	# Load the various data for optimization
	S.loadPokemonData('GAME_MASTER.json')
	S.loadMoveData('GAME_MASTER.json')
	S.loadUserData('Master.csv')

	# Run the optimization for selecting
	S.optimize('STEEL', 'FIGHTING')


# Main loop
if __name__ == '__main__':
	main()
