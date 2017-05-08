#execfile('/Users/yiwen/Desktop/try.py')

import vtk
import math

filename ="/Users/yiwen/Desktop/brain.png"
reader=vtk.vtkPNGReader()
reader.SetFileName(filename)
reader.Update()


image_out = reader.GetOutputPort()


resample=vtk.vtkImageReslice()
resample.SetInputConnection(image_out)
resample.SetOutputSpacing(0.20,0.20,0)
resample.Update()






def sinc(x):
    return (math.sin(math.pi * x) / (math.pi * x))

    
def sincint(x,y,n,m):
    if (x == n) or (m == y):
       return 1.0
    else:
       a =(sinc(x-n)**2  + sinc(y-m)**2)**0.5
       return a

def drange(start, stop, step):
    r = start
    while r < stop:
         yield r
         r += step

def round_pixel(p):
    if p - math.floor(p) <= 0.5:
       return int(math.floor(p))
    else:
       return int(math.ceil(p))
    
image= resample.GetOutput()


for i in range(120,240):
  for k in range(540,610):
    new_value=0
    weight = 0
    for n in drange(i-9,i+9,0.4):  #interval cannot be divisible by step!!!!!
      for m in drange(k-9,k+9,0.4):
          new = sincint(i,k,n,m)
          #print "weight at ", n," ", m, "is ", new
          pvalue=image.GetScalarComponentAsDouble(int(math.floor(n)),int(math.floor(m)),0,0)
          weight = weight + new  
          new_value  = new * pvalue + new_value
    #print "total weight at ", n, " ", m, " is ", weight 
    for j in range(0,3):
      image.SetScalarComponentFromDouble(i,k,0,j,new_value / weight)
   # print image.GetScalarComponentAsDouble(i,k,0,0)
          


#print image.GetScalarComponentAsDouble(800,1900,0,0)


writer=vtk.vtkPNGWriter()
writer.SetFileName('brain_5_03.png')
writer.SetInputData(image)
writer.Update()
writer.Write()

