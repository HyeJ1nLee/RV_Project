import imutils
import cv2
import pytesseract 
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe' 

image = cv2.imread("car4.jpg")
(h, w, d) = image.shape

cv2.imshow("Image", image)
img = imutils.resize(image, width=500 ) #이미지 가로 사이즈가 500이 되도록 조절 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #그레이 스케일

a = cv2.Canny(gray, 30, 200)
cv2.imwrite("no_blur.png",a)
gray = cv2.GaussianBlur(gray,(3,3),5) #가우시안 블러 처리
cv2.imshow("GaussianBlur",gray)

edged = cv2.Canny(gray, 30, 200) #treshold 값을 30,200d으로 지정하여 캐니 에지 검출
cv2.imshow("Canny",edged)

cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #Contour 검출
img1=img.copy() 

cv2.drawContours(img1,cnts,-1,(0,255,0),3) #검출한 Contour 그리기
cv2.imshow("img1",img1) 

cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:30] #면적순으로 Contour 30개 추출
screenCnt = None #will store the number plate contour 
img2 = img.copy() 
cv2.drawContours(img2,cnts,-1,(0,255,0),3)  
cv2.imshow("img2",img2) #top 30 contours 


idx=7
# loop over contours
for c in cnts:
  # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        if len(approx) == 4: #chooses contours with 4 corners
                screenCnt = approx
                x,y,w,h = cv2.boundingRect(c) #finds co-ordinates of the plate
                new_img=img[y:y+h,x:x+w]
                cv2.imwrite('number.png',new_img) #stores the new image
                idx+=1
                break

#draws the selected contour on original image        
cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
cv2.imshow("Final image with plate detected",img)
Cropped_loc='number.png' #the filename of cropped image
cv2.imshow("cropped",cv2.imread(Cropped_loc)) 

text=pytesseract.image_to_string(Cropped_loc,lang='kor', config='') #이미지내 텍스트를 문자열로 바꿈
"""arr = text.split('\n')[0:-1]
text = '\n'.join(arr)"""
print("차량 번호:" ,text)
cv2.waitKey(0)
cv2.destroyAllWindows() 