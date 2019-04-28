import random
from PIL import Image, ImageDraw, ImageFilter
import timeit
import requests, json
# https://curl.trillworks.com/
data = '{"model":"default"}'

response = requests.post('http://colormind.io/api/', data=data)
colors = dict(response.json())['result']

print(colors)
tic=timeit.default_timer() #start timer
dim1=600
dim2=400


#colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'orange', 'black', 'yellow', 'white']
 #instantiate list of colors and open files
im = Image.new('RGBA', (dim1, dim2), 'white')
pix = im.load()

origin1=(dim1/2)-25+(random.randint(0,50))
origin2=(dim2/2)-25+(random.randint(0,50)) #origin coordinates to generate in 4 sectors

def randrgb():
    return int(random.randint(0,255))
def randcolor():         
    r = random.randint(0,len(colors)-1)  #random generators
    #print(str(r) + ' '+ str(len(colors)))
    return tuple(colors[r])


draw = ImageDraw.Draw(im)


for a in range(dim1):
    draw.point([a,0], fill=randcolor())
    draw.point([a,400], fill=randcolor())
for b in range(dim2):     #seed the png
    draw.point([0,b], fill=randcolor())
    draw.point([600,b], fill=randcolor())
    

def zebra(d1, d2, startX, startY):
    for a in range(startX,d1):
        for b in range(startY,d2):
            p1=pix[a-1,b]
            p2=pix[a-1,b-1]
            p3=pix[a,b-1]
            if((p1==p2)):
                draw.point([a,b], fill=p1)       #the magic <3
            elif(p1==p3):
                draw.point([a,b], fill=p3)
            elif(p2==p3):
                draw.point([a,b], fill=p2)
            else:
                draw.point([a,b], fill=randcolor())
       
                
def pollock(d1, d2, startX, startY):
       for a in range(startX,d1):
          for b in range(startY,d2):
            p1=pix[a-1,b]
            p2=pix[a-1,b-1]
            p3=pix[a,b-1] 
            
            if(randrgb()<250):
                if((p1==p2)):
                    draw.point([a,b], fill=p1)       #the magic <3
                elif(p1==p3):
                    draw.point([a,b], fill=p3)
                elif(p2==p3):
                    draw.point([a,b], fill=p2)
                else:
                    draw.point([a,b], fill=randcolor())
            else:
                draw.point([a,b], fill=randcolor())

def colorswab(d1,d2,x,y, number):  #start xy, end xy
    xy=[]
    for b in range(1,number):  #number of shapes         
        for c in range(0,random.randint(3,7)): #number of sides
            xy.append(random.randint(x,d1))
            xy.append(random.randint(y,d2)) #draws random sided polygons

        draw.polygon(xy, fill=randcolor())
        



if(int(random.randint(0,100))<90):
    pollock(dim1,dim2,1,1)
    im = im.filter(ImageFilter.GaussianBlur(radius=2))
    colorswab(dim1,dim2,1,1,5)

else:
    pollock(dim1,dim2,1,1)


file = open('iter.txt')
num = int(file.read()) #get number of tests
file.close()
file = open('iter.txt', 'w')
num+=1 
im.save('test'+str(num)+'.png')
print('test image #'+str(num))
file.write(str(num))
file.close()

toc=timeit.default_timer()

print('Generated in '+str(toc-tic)[:5]+' seconds')
