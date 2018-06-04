import numpy as np
import cv2
import os
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw


import cv2 as cv

def detectDeleteIcon(path):
	"""
	Detect the delete icon in the screenshot and check for guidelines
	"""
	deletePath = path + "/Delete"
	images = os.listdir(deletePath)
	fileName = ["icon", "delete"]

	for i, image in enumerate(images[1: (len(images) / 2)+1]):

		print(deletePath + "/" + fileName[0] + str(i+1) + "." + image.split('.')[1])
		print(deletePath + "/" + fileName[1] + str(i+1) + "." + image.split('.')[1])

		img1 = cv2.imread(deletePath + "/" + fileName[0] + str(i+1) + "." + image.split('.')[1], 0) # queryImage
		img2 = cv2.imread(deletePath + "/" + fileName[1] + str(i+1) + "." + image.split('.')[1], 0) # trainImage

		# Initiate SIFT detector
		sift = cv2.xfeatures2d.SIFT_create()

		# find the keypoints and descriptors with SIFT
		kp1, des1 = sift.detectAndCompute(img1,None)
		kp2, des2 = sift.detectAndCompute(img2,None)

		# BFMatcher with default params
		bf = cv2.BFMatcher()
		matches = bf.knnMatch(des1,des2, k=2)

		# Apply ratio test
		good = []
		goodMatches = []
		for m,n in matches:
		    if m.distance < 0.80*n.distance:
		        good.append([m])
		        goodMatches.append(m)

		# Initialize lists
		list_kp2 = []

		# For each match...
		for mat in goodMatches:

		    # Get the matching keypoints for each of the images
		    img2_idx = mat.trainIdx

		    # x - columns
		    # y - rows
		    # Get the coordinates
		    (x2,y2) = kp2[img2_idx].pt

		    # Append to each list
		    list_kp2.append((x2, y2))

		pointArray = np.array(list_kp2)
		xs = pointArray[:,0]
		ys = pointArray[:,1]

		minX = int(np.min(xs))
		minY = int(np.min(ys))
		maxX = int(np.max(xs))
		maxY = int(np.max(ys))

		print(list_kp2)
		img2 = cv.rectangle(img2, (minX, minY), (maxX, maxY), (0,0,255), 2)
		f = open(path + "/textResults" + "/delResult" + str(i) + ".html", "w+") 

		# f.write("\nThe position of the delete icon in the original pic is: ")
		# f.write(str(list_kp2[0]))

		icon = Image.open(deletePath + "/" + fileName[0] + str(i+1) + "." + image.split('.')[1])
		main = Image.open(deletePath + "/" + fileName[1] + str(i+1) + "." + image.split('.')[1])
		widthIcon, heightIcon = icon.size
		areaIcon = widthIcon * heightIcon / 2

		widthMain, heightMain = main.size
		# f.write("\nChecking position of the delete icon")

		if(list_kp2[0][0] > (0.66) * widthMain and list_kp2[0][1] > (0.66) * heightMain):
			f.write("\nDelete Icon is in the right spot (away from the home)")
		else:
			f.write("\nMove the delete icon away from the home button")

		f.close()

		source = Image.open(deletePath + "/" + fileName[1] + str(i+1) + "." + image.split('.')[1]).convert("RGBA")
		draw = ImageDraw.Draw(source)
		draw.rectangle(((minX-6, minY-6), (maxX+6, maxY+6)), outline="black")
		source.save(path + '/Results' + '/delResult'+ str(i) +'.jpeg', "JPEG")		

		img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)
		img = Image.fromarray(img3, 'RGB')
		img.save(path + '/Results' + '/delResult'+ str(i+10) +'.png')
		img.show()
		
		plt.imshow(img3),plt.show()


def detectSearchIcon(path):
	"""
	Detect the search icon in the screenshot and check for guidelines
	"""
	searchPath = path + "/Search"
	images = os.listdir(searchPath)
	fileName = ["icon", "search"]

	for i, image in enumerate(images[1: (len(images) / 2)+1]):

		print(searchPath + "/" + fileName[0] + str(i+1) + "." + image.split('.')[1])
		print(searchPath + "/" + fileName[1] + str(i+1) + "." + image.split('.')[1])

		img1 = cv2.imread(searchPath + "/" + fileName[0] + str(i+1) + "." + image.split('.')[1], 0) # queryImage
		img2 = cv2.imread(searchPath + "/" + fileName[1] + str(i+1) + "." + image.split('.')[1], 0) # trainImage

		# Initiate SIFT detector
		sift = cv2.xfeatures2d.SIFT_create()

		# find the keypoints and descriptors with SIFT
		kp1, des1 = sift.detectAndCompute(img1,None)
		kp2, des2 = sift.detectAndCompute(img2,None)

		# BFMatcher with default params
		bf = cv2.BFMatcher()
		matches = bf.knnMatch(des1,des2, k=2)

		# Apply ratio test
		good = []
		goodMatches = []
		for m,n in matches:
		    if m.distance < 0.725*n.distance:
		        good.append([m])
		        goodMatches.append(m)

		# Initialize lists
		list_kp2 = []

		# For each match...
		for mat in goodMatches:

		    # Get the matching keypoints for each of the images
		    img2_idx = mat.trainIdx

		    # x - columns
		    # y - rows
		    # Get the coordinates
		    (x2,y2) = kp2[img2_idx].pt

		    # Append to each list
		    list_kp2.append((x2, y2))

		pointArray = np.array(list_kp2)
		xs = pointArray[:,0]
		ys = pointArray[:,1]

		print(xs)
		print(ys)

		minX = int(np.min(xs))
		minY = int(np.min(ys))
		maxX = int(np.max(xs))
		maxY = int(np.max(ys))

		f = open(path + "/textResults" + "/searchResults" + str(i) + ".html", "w+") 
		# f.write("The position of the search icon in the original pic is: ")

		icon = Image.open(searchPath + "/" + fileName[0] + str(i+1) + "." + image.split('.')[1])
		main = Image.open(searchPath + "/" + fileName[1] + str(i+1) + "." + image.split('.')[1])
		widthIcon, heightIcon = icon.size
		areaIcon = widthIcon * heightIcon / 2

		widthMain, heightMain = main.size
		# f.write("\nChecking position of the search icon")

		# f.write(str(list_kp2[0][1]))
		
		if(list_kp2[0][1] < (0.33) * heightMain):
			f.write("\nSearch Icon is in the right spot")
		else:
			f.write("\nMove the search icon above")

		thresholdArea = 38 * 38 / 4

		# f.write("\nChecking the size of the search icon")
		if(areaIcon > thresholdArea):
			f.write("\nCool Search Icon!")
		else:
			f.write("\nCan't see the Icon :(")

		f.close()

		source = Image.open(searchPath + "/" + fileName[1] + str(i+1) + "." + image.split('.')[1]).convert("RGBA")
		draw = ImageDraw.Draw(source)
		draw.rectangle(((minX-8, minY-8), (maxX+8, maxY+8)), outline="black")
		source.save(path + '/Results' + '/searchResults'+ str(i) + '.png', "PNG")

		# cv2.drawMatchesKnn expects list of lists as matches.
		img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)
		img = Image.fromarray(img3, 'RGB')
		img.save(path + '/Results' + '/searchResult'+ str(i+10) + '.png')
		img.show()
		plt.imshow(img3),plt.show()


if __name__ == '__main__':

	path = "Pics"
	detectDeleteIcon(path)
	detectFonts(path)





