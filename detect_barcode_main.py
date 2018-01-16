# import the necessary packages
from pyimagesearch import simple_barcode_detection
import argparse
import cv2
from pyzbar.pyzbar import decode
from PIL import Image
import pytesseract

# Global Variables: 
x_cor = 0
y_cor = 0
h_cor = 0
w_cor = 0
num_of_frames = 0 
final_frame =0

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help = "path to the (optional) video file")
args = vars(ap.parse_args())

# if the video path was not supplied, grab the reference to the
# camera
if not args.get("video", False):
	camera = cv2.VideoCapture(1)

# otherwise, load the video
else:
	camera = cv2.VideoCapture(args["video"])

# keep looping over the frames
count =0
while count < 20:
	# grab the current frame
	(grabbed, frame) = camera.read()
	#cv2.imwrite("before %d"%count + '.jpg', frame) 	
	# check to see if we have reached the end of the
	# video
	if not grabbed:
		break
	
	if (count == 0 and final_frame ==0):
		frame2 = frame
		cv2.imwrite("Clean_Frame.jpg", frame2)
		
	# detect the barcode in the image
	box = simple_barcode_detection.detect(frame)


	#file = open("data.txt","a") 
	#file.write(str(box[0]))
	#file.write(str(box[1]))
	#file.write(str(box[2]))
	#file.write(str(box[3]))
	#file.write("\n------------------------%d-----------------------------\n"% count)
	#file.close()  

	# if a barcode was found, draw a bounding box on the frame
	cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)

	# Firas TEST
	x,y,w,h = cv2.boundingRect(box)
	#print (x,y,w,h)
	x_cor = x_cor + x
	y_cor = y_cor + y
	w_cor = w_cor + w
	h_cor = h_cor + h
	num_of_frames =num_of_frames+1

	#roi=frame[y:y+h,x:x+w]
	#cv2.imwrite(str(count) + '.jpg', roi)
	
	# show the frame and record if the user presses a key
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	#cv2.imwrite("frame%d.jpg" % count, frame)


	count = count+1
	

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

#print (frame2)
#print ("\n --------------:\n")

frame2 = cv2.imread('Clean_Frame.jpg')
x_cor_avg = int (x_cor/num_of_frames)
y_cor_avg = int (y_cor/num_of_frames)
w_cor_avg = int (w_cor/num_of_frames) 
h_cor_avg = int (h_cor/num_of_frames) 

#print (y_cor_avg,h_cor_avg,x_cor_avg,w_cor_avg)
#roi=frame2[y_cor_avg:y_cor_avg+h_cor_avg,x_cor_avg:x_cor_avg+w_cor_avg]
roi=frame2[y_cor_avg - 20 :y_cor_avg+h_cor_avg +20,x_cor_avg -20 :x_cor_avg+w_cor_avg +20]
#roi = frame2[200:800, 100:400]
cv2.imwrite("final" + '.jpg', roi)
cv2.imshow("cropped", roi)

# The serial number part: 
serial_number = decode(Image.open('C:/Users/NAHIR/Google Drive/Pannon/Project_lab/Final/final.jpg'))
print ("The serial number is:",serial_number[0][0].decode('utf-8', 'ignore'))

#pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
#print(pytesseract.image_to_string(Image.open('Clean_Frame.jpg')))

cv2.waitKey(0)

#roi=frame[y:y+h,x:x+w]
#cv2.imwrite("test" + '.jpg', roi)
# cleanup the camera and close any open windows




camera.release()
cv2.destroyAllWindows()


#print (x_cor_avg,y_cor_avg,w_cor_avg,h_cor_avg)
#print (count)
#print (num_of_frames)
#roi=frame[y_cor_avg:y_cor_avg+h_cor_avg,x_cor_avg:x_cor_avg+w_cor_avg]

#cv2.imwrite("final" + '.jpg', roi)
