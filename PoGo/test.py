import pandas as pd
import numpy as np
import math
import json
import re

class processData:
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

	def optimize(self, defTypeA, defTypeB, defDef):
		tt = 30
		happyList = []
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
				# Retrieve some values
				qIdx = self.moveData.index[self.moveData['uniqueID'] == qMove][0]
				qType = self.moveData['type'][qIdx]
				qPower = self.moveData['power'][qIdx]
				qEnergy = self.moveData['energyDelta'][qIdx]
				qDuration = self.moveData['duration'][qIdx]

				# qDPS = self.moveData['DPS'][qIdx]
				# qEPS = self.moveData['EPS'][qIdx]

				# Update qPower
				qPower = self.typeBonus(qPower, qType, atkTypeA, atkTypeB, defTypeA, defTypeB)

				# print(qMove, qDPS, qEPS, qType)

				qNum100 = math.ceil(abs(100.0 / qEnergy))
				qDmg = qPower * qNum100
				qTime = qDuration * qNum100


				for cMove in chargeMoves:
					# Make a dictionary row
					dictRow = {}

					# Store the moves
					dictRow['Name'] = qMove.replace('_',' ').replace('FAST','') + '& ' + cMove.replace('_',' ')

					# Retrieve some values
					cIdx = self.moveData.index[self.moveData['uniqueID'] == cMove][0]
					cEnergy = self.moveData['energyDelta'][cIdx]
					cPower = self.moveData['power'][cIdx]
					cType = self.moveData['type'][cIdx]
					cDuration = self.moveData['duration'][cIdx]

					# Update qPower
					cPower = self.typeBonus(cPower, qType, atkTypeA, atkTypeB, defTypeA, defTypeB)


					cNum100 = math.floor(abs(100.0 / cEnergy))
					cDmg = cPower * cNum100
					cTime = cDuration * cNum100


					# Total DPS
					DPS = (qDmg + cDmg) / (qTime + cTime)
					DPS = atkCurrent/200 * DPS

					dictRow['DPS'] = DPS

					dictList.append(dictRow)

			maxDPS = max(dictList, key=lambda x:x['DPS'])
			self.userData['Moveset'][ii] = maxDPS['Name']
			self.userData['DPS'][ii] = maxDPS['DPS']

		# print(dictRow)
		# df['High'].nlargest(2)

		# print(self.userData.head(10))
		test2 = self.userData.sort_values(by=['DPS'], ascending=False)
		print(test2.head(20))

def main():
	# Set up classes
	P = processData()

	# Load the various data
	P.loadPokemonData('GAME_MASTER.json')
	P.loadMoveData('GAME_MASTER.json')
	P.loadUserData('Master.csv')

	# Run the optimization
	defTypeA = 'STEEL'
	defTypeB = 'FIGHTING'
	defDef = 200
	P.optimize(defTypeA, defTypeB, defDef)

	# power = 15
	# multipliers = 1.2
	# print('Rayquaza', math.floor(0.5 * power * (284 / defDef) * multipliers) + 1)

# Main loop
if __name__ == '__main__':
	main()
