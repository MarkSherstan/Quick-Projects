import pandas as pd
import numpy as np
import pytesseract
import imutils
import glob
import cv2

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
		ROI = self.GRAY[900:1020, 275:850]

		# Threshold and invert the image
		_, ROI = cv2.threshold(ROI, 200, 255, cv2.THRESH_BINARY)

		# OCR the name
		self.ID = str(pytesseract.image_to_string(ROI)) + str(self.CP)

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
		ROI = self.GRAY[120:240, 340:730]

		# Remove background by thresholding
		_, ROI = cv2.threshold(ROI, 250, 255, cv2.THRESH_BINARY)
		ROI = cv2.cvtColor(ROI, cv2.COLOR_GRAY2RGB)

		# Erode and dialte the image to get rid of CP and make readable
		kernel = np.ones((2,2),np.uint8)
		ROI = cv2.erode(ROI, kernel, iterations = 2)
		ROI = cv2.dilate(ROI, kernel, iterations = 4)

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
			self.FTM = moves[0]
			self.CTM1 = moves[1]
			self.CTM2 = moves[2]
		elif len(moves) is 2:
			self.FTM = moves[0]
			self.CTM1 = moves[1]

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
				'Fast Attack', 'Charge Attack 1', 'Charge Attach 2'])

			df.to_csv(fileName, index=None, header=True)
			print('File saved to:\t' + fileName)

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
				'DEF_IV', 'STA_IV', 'Percent IV', 'Catch Data', 'Catch Location'])

			df.to_csv(fileName, index=None, header=True)
			print('File saved to:\t' + fileName)

def main():
	G = getData()

	# Log data -> Filename, printFlag, csvFlag
	G.logDataA('dataA.csv', True, True)
	G.logDataB('dataB.csv', True, True)

# Main loop
if __name__ == '__main__':
	main()
