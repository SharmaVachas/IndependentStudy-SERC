import pytesseract
import os
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

# '/home/kaushik/Pictures/Pics/Submit/temp2.jpg'

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def findSubmitButton(path):
	"""
	Finds the submit button in the given picture
	"""
	submitButtonPath = path + "/Submit"
	imageFiles = os.listdir(submitButtonPath)

	for k, image in enumerate(imageFiles):
		im = Image.open(submitButtonPath + "/" + image)
		text = pytesseract.image_to_string(Image.open(submitButtonPath + "/" + image))
		a = pytesseract.image_to_boxes(Image.open(submitButtonPath + "/" + image))
		all_co_ordinates = a.split('0\n')

		letter_position = {}
		for i in all_co_ordinates:
			co_ordinates = i.split(' ')
			res = []
			for j, val in enumerate(co_ordinates[1:-1]):
				res.append(int(val))

				try:
					if(is_ascii(str(co_ordinates[0]))):
						letter_position[str(co_ordinates[0]).lower()] = res
				except:
					pass

		f = open(path + "/textResults" + "/submitResults" + str(k) + ".html", "w+") 
		# f.write("\nChecking for Submit Button Guidelines")
		try:
			spos = letter_position['s'] 
			tpos = letter_position['t']

			area = (tpos[2] - spos[0]) * (tpos[3] - spos[1])
			if(area > 3000):
				print("\nInsanely Huge Button!!")
			elif(area < 1000):
				print("\nWay too small button!")

			width, height = im.size
			
			if(spos[0] > (2 / 3) * height):
				print("\nSubmit button is in a nice spot")
			else:
				print("\nPlease move submit button lower")

			source = Image.open(submitButtonPath + "/" + image).convert("RGBA")
			draw = ImageDraw.Draw(source)
			
			draw.rectangle(((spos[0], spos[1]+235), (tpos[2], tpos[3]+235)), outline="black")
			source.save(path + '/Results' + '/submitResults'+ str(k) + '.jpg', "JPEG")
			source.show()
		except:
			pass

if __name__ == '__main__':
	# path = raw_input("Image Source: ")
	path = "."
	findSubmitButton(path)


