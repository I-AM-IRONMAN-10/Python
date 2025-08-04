import cv2 as c
import numpy as np 
import matplotlib.pyplot as plt 

# Read the image
img=c.imread("/Users/santoshr/Downloads/dc vs lsg.webp") 
def rotate(img,angle,rotatepoint=None):
    (height,width)=img.shape[:2]

    if rotatepoint is None:
        rotatepoint=(width//2,height//2)
    rotMat =c.getRotationMatrix2D(rotatepoint,angle,1.0) 
    dimention=(width,height)
    
    return c.warpAffine(img,rotMat,dimention)

c.imshow("CRICKET",img) 
key=c.waitKey(0)
if key==ord("R") or key == ord("r"):
    print("VARTA MAME DUUR")
    c.destroyAllWindows()
grey=c.cvtColor(img,c.COLOR_BGR2GRAY)
c.imshow("Gray",grey)
kl=c.waitKey(0)
if kl==ord("S") or kl==ord("s"):
    print("wait panru da ...")
    c.destroyAllWindows()

blur=c.GaussianBlur(img,(7,7),c.BORDER_DEFAULT)
c.imshow("blur",blur)
km=c.waitKey(0)
if km==ord("m") or km==ord("M"):
    c.destroyAllWindows()


canny=c.Canny(blur,50,50)
c.imshow("outline",canny)
kml=c.waitKey(0)
if kml==ord("L") or kml==ord("l"):
    c.destroyAllWindows()

dilated=c.dilate(img,(3,3),iterations=1)
c.imshow("dialated",dilated)
kc=c.waitKey(0)

rotated=rotate(img,45)
c.imshow("ROTATED",rotated)

c.waitKey(0)
couter,h=c.findContours(canny,c.RETR_LIST,c.CHAIN_APPROX_SIMPLE)
print(f"{len(couter)} is found ")

b, g, r = c.split(img)
c.imshow("blue",b)
c.waitKey(0)
c.imshow("green",g)
c.waitKey(0)
c.imshow("red",r)

c.waitKey(0)

average = c.blur(img,(3,3))
c.waitKey(0)

gaussian_blur = c.GaussianBlur(img,(3,3))
c.waitKey(0)


blank = np.zeros((400,400),dtype="uint8")
rectangle = c.rectangle(blank.copy(),(30,30),(370,370),255,-1)
circle = c.circle(blank.copy(),(200,200),200,255,-1)

c.imshow("rectangle", rectangle)
c.imshow("circle", circle)

bit_wise = c.bitwise_and(rectangle, circle)
c.imshow("bit_and", bit_wise)

bit_wise1 = c.bitwise_not(rectangle)  # <-- FIXED
c.imshow("bit_not", bit_wise1)

bit_wise2 = c.bitwise_or(rectangle, circle)
c.imshow("bit_or", bit_wise2)

bit_wise3 = c.bitwise_xor(rectangle, circle)
c.imshow("bit_xor", bit_wise3)

n = c.waitKey(0)
if n == ord("A") or n == ord("a"):
    c.destroyAllWindows()
    blank = np.zeros(img.shape[:2],dtype="uint8")
mask = c.circle(blank,(img.shape[1]//2,img.shape[0]//2),100,255,-1)
c.imshow("mask",mask)
masked = c.bitwise_and(img,img,mask=mask)
c.imshow("masked",masked)
c.imshow("blank",blank)
c.waitKey(0)
grey = c.cvtColor(img,c.COLOR_BGR2RGB)
c.imshow("grey",grey)

grey_hist = c.calcHist([grey],[0],None,[256],[0,256])
plt.title("hist")
plt.xlabel("san")
plt.ylabel("fig")
plt.plot(grey_hist)
plt.show()

#lapsian edge 

lap = c.Laplacian(grey,c.CV_64F)
lap = np.uint8(np.absolute(lap))

c.imshow("lap",lap)

sobelx = c.Sobel(grey,c.CV_64F,1,0)
sobely = c.Sobel(grey,c.CV_64F,0,1)

c.imshow("sobelx",sobelx)
c.imshow("sobely",sobely)
sobel_combine= c.bitwise_or(sobelx,sobely)

c.imshow("combined image",sobel_combine)
c.waitKey(10000)
