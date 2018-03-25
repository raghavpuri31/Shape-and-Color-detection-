#classes and subclasses to import
import cv2
from collections import OrderedDict
import numpy as np
import os,math,time

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#subroutine to write rerults to a csv
def writecsv(color,shape,size,count):
    #open csv file in append mode
    filep = open('results1B_2875.csv','a')
    # create string data to write per image
    datastr = "," + color + "-" + shape + "-" + size + "-" + count
    #write to csv
    filep.write(datastr)

def main(path):
#####################################################################################################
    data=[]
    objectcounter={}
    storeit=False
    if os.name=="nt":
        filename=path.split("\\")[-1]
    else:
        filename=path.split("/")[-1]
    #print filename
    if filename.startswith("Sample"):
        samplesize=filename.split("_")[-1]
        samplesize=samplesize.split(".")[0]
        storeit=True
    data.append(filename)
    """for (i, (name, rgb)) in enumerate(colors.items()):
        lab_col[i] = rgb
        colorNames.append(name)"""
    #lab_col = cv2.cvtColor(lab_col, cv2.COLOR_RGB2LAB)
    image = cv2.imread(path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# define range of  color in HSV
    lr = np.array([0,100,100])
    ur = np.array([10,255,255])
    lg = np.array([50,100,100])
    ug = np.array([70,255,255])
    lb = np.array([110,50,50])
    ub = np.array([130,255,255])
    ly = np.array([20,100,100])
    uy = np.array([40,255,255])
    lo = np.array([5,100,100])
    uo = np.array([25,255,255])
    colours = ( lr , ur , lg , ug , lb , ub , ly , uy , lo , uo )
    colour = ('red' ,'green','blue','yellow','orange')
    #count=-1
    def func(i,maskq) :
        gray = cv2.cvtColor(maskq, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(maskq, 150, 255,cv2.THRESH_BINARY)[1]
        edge = cv2.Canny(thresh, 0, 255)
        cnts = cv2.findContours(edge, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[1]
        #print len(cnts)
        for c in cnts:
            #count+=1
            M = cv2.moments(c)
            try:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"]) 
            except:
                cX=0
                cY=0
            x = cX+1
            y = cY+1
            shape = "unidentified"
            peri = cv2.arcLength(c, True)
            area=cv2.contourArea(c)
            #print colour[i],peri,area
            if peri<100 or area<100:
                continue
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)
            if len(approx) == 3:
                    (x, y, w, h) = cv2.boundingRect(approx)
                    area=0.5*w*h
                #print color+"--Triangle----",area
                    shape = "Triangle"
                    color = colour[i]
                    if globally.get(shape) and globally[shape].get("large") and globally[shape].get("small"):
                        if area>=globally[shape]["large"]:
                            size="Large"
                        elif area<=globally[shape]["small"]:
                            size="Small"
                        else:
                            size="Medium"
                    else:
                        size="Sample size not present"
            elif len(approx) == 4:
                    (x, y, w, h) = cv2.boundingRect(approx)
                    ar = w / float(h)
                    area=w*h
                    shape = "Square" if ar >= 0.95 and ar <= 1.05 else "Rectangle"
                    color=colour[i]
                    if globally.get(shape) and globally[shape].get("large") and globally[shape].get("small"):
                        if area>=globally[shape]["large"]:
                            size="Large"
                        elif area<=globally[shape]["small"]:
                            size="Small"
                        else:
                            size="Medium"
                    else:
                        size="Sample size not present"
            else:
                    _,radius=cv2.minEnclosingCircle(c)
                    area=3.14*radius*radius
                    shape = "Circle"
                    color=colour[i]
                    if globally.get(shape) and globally[shape].get("large") and globally[shape].get("small"):
                        if area>=globally[shape]["large"]:
                            size="Large"
                        elif area<=globally[shape]["small"]:
                            size="Small"
                        else:
                            size="Medium"
                    else:
                        size="Sample size not present"
            c = c.astype("int")
            text = "{} {}".format(color, shape)
            cv2.drawContours(image, [c], -1, (0, 0, 0), 2)
            cv2.putText(image, text, (x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            if storeit==True:
                globally.setdefault(shape,{})
                globally[shape].setdefault(samplesize,area)
            else:
                if [color+"-"+shape+"-"+size+"-"+str(objectcounter.get(shape+"_"+color+"_"+size,1))] in data:
                    index=data.index([color+"-"+shape+"-"+size+"-"+str(objectcounter[shape+"_"+color+"_"+size])])
                    objectcounter[shape+"_"+color+"_"+size]+=1
                    data[index]=[color+"-"+shape+"-"+size+"-"+str(objectcounter[shape+"_"+color+"_"+size])]
                else:
                    objectcounter[shape+"_"+color+"_"+size]=1
                    data.append([color+"-"+shape+"-"+size+"-"+str(objectcounter[shape+"_"+color+"_"+size])])
        return
    k = 0
    mask = cv2.inRange(hsv,lr,ur)
    if mask.any() == True :
        res = cv2.bitwise_and(image,image, mask= mask)
        func (k,res);
    k += 1
    mask = cv2.inRange(hsv,lg,ug)
    if mask.any() == True :
        res = cv2.bitwise_and(image,image, mask= mask)
        func (k,res);
    k += 1
    mask = cv2.inRange(hsv,lb,ub)
    if mask.any() == True :
        res = cv2.bitwise_and(image,image, mask= mask)
        func (k,res);
    k += 1
    mask = cv2.inRange(hsv,ly,uy)
    if mask.any() == True :
        res = cv2.bitwise_and(image,image, mask= mask)
        func (k,res);
    k += 1
    mask = cv2.inRange(hsv,lo,uo)
    if mask.any() == True :
        res = cv2.bitwise_and(image,image, mask= mask)
        func (k,res);
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    if not storeit:
        cv2.imwrite("Output"+filename.split(".")[0][-1]+".png",image)
        for i in data[1:]:
                properties=i[0].split("-")
                writecsv(properties[0],properties[1],properties[2],properties[3])
    return data
#####################################################################################################


#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    globally={}
    mypath = '.'
    #getting all files in the directory
    onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if f.endswith(".png") and f.startswith("test")]
    mypath="Sample Images"
    onlyfiles.append([os.path.join(mypath, f) for f in os.listdir(mypath) if f.endswith(".png")])
    #deleting files previously created so that it does not read those again
    try:
        os.remove('results1B_teamid.csv')
    except:
        pass
    #iterate over each file in the sample directory
    for fp in onlyfiles[-1]:
        data=main(fp)
    #iterate over each file in the sample directory
    for fp in onlyfiles[:-1]:
        #Open the csv to write in append mode
        filep = open('results1B_teamid.csv','a')
        #this csv will later be used to save processed data, thus write the file name of the image 
        filep.write(fp.split("/")[-1])
        #close the file so that it can be reopened again later
        filep.close()
        #process the image
        data = main(fp)
        print data
        #open the csv
        filep = open('results1B_teamid.csv','a')
        #make a newline entry so that the next image data is written on a newline
        filep.write('\n')
        #close the file
        filep.close()
