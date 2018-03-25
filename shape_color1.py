#classes and subclasses to import
import cv2
from collections import OrderedDict
import numpy as np
import os

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#subroutine to write rerults to a csv
def writecsv(color,shape):
    #open csv file in append mode
    filep = open('results1A_2875.csv','a')
    # create string data to write per image
    datastr = "," + color + "-" + shape
    #write to csv
    filep.write(datastr)

def main(path):
#####################################################################################################
    colors = OrderedDict({"Red": (255, 0, 0),"Green": (0, 255, 0),"Blue": (0, 0, 255)})
    lab_col = np.zeros((len(colors), 1, 3), dtype="uint8")
    colorNames = []
    data=[]
    if os.name=="nt":
        filename=path.split("\\")[-1]
    else:
        filename=path.split("/")[-1]
    data.append(filename)
    for (i, (name, rgb)) in enumerate(colors.items()):
        lab_col[i] = rgb
        colorNames.append(name)
    lab_col = cv2.cvtColor(lab_col, cv2.COLOR_RGB2LAB)
    image = cv2.imread(path)
    resized = cv2.resize(image,(450,300))
    ratio = image.shape[0] / float(resized.shape[0])
    blurred = cv2.GaussianBlur(resized, (5, 5), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
    thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_TRUNC)[1]
    edged = cv2.Canny(thresh, 0, 255)
    x,cnts,hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    count=-1
    for c in cnts:
        count+=1
        if hierarchy[0][count][0]==-1 and not hierarchy[0][count][3] ==-1:
            if hierarchy[0][count][1]==-1:
                continue
            if hierarchy[0][count][2]==-1:
                continue
            elif hierarchy[0][count][2]<count:
                continue
        M = cv2.moments(c)
        try:
            cX = int((M["m10"] / M["m00"]) * ratio)
            cY = int((M["m01"] / M["m00"]) * ratio)
        except:
            cX=0
            cY=0
	#color detection 
        mask = np.zeros(lab.shape[:2], dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.erode(mask, None, iterations=2)
        mean = cv2.mean(lab, mask=mask)[:3]
        minDist = (np.inf, None)
        for (i, row) in enumerate(lab_col):
            d = sum([(x-y)**2 for (x,y) in zip(row[0],mean)])**(0.5)
            if d < minDist[0]:
                minDist = (d, i)
        color=colorNames[minDist[1]]
	#shape detection
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        if len(approx) == 3:
            shape = "triangle"
        elif len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
        elif len(approx) == 5:
            shape = "pentagon"
        else:
            shape = "circle"
        c = c.astype("float")
        c *= ratio
        c = c.astype("int")
        text = "{} {}".format(color, shape)
        cv2.drawContours(image, [c], -1, (0, 0, 0), 2)
        cv2.putText(image, text, (cX, cY),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        writecsv(color,shape)
        data.append([color+"-"+shape])
    #cv2.imshow("Image", image)
    #cv2.waitKey(0)
    cv2.imwrite("Output"+filename.split(".")[0][-1]+".png",image)
    return data
#####################################################################################################


#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    mypath = '.'
    #getting all files in the directory
    onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if f.endswith(".png") and f.startswith("test")]
    #deleting files previously created so that it does not read those again
    try:
        os.remove('results1A_teamid.csv')
    except:
        pass
    #iterate over each file in the directory
    for fp in onlyfiles:
        #Open the csv to write in append mode
        filep = open('results1A_teamid.csv','a')
        #this csv will later be used to save processed data, thus write the file name of the image 
        filep.write(fp.split("/")[-1])
        #close the file so that it can be reopened again later
        filep.close()
        #process the image
        data = main(fp)
        print data
        #open the csv
        filep = open('results1A_teamid.csv','a')
        #make a newline entry so that the next image data is written on a newline
        filep.write('\n')
        #close the file
        filep.close()
