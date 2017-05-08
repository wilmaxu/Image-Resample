 #execfile('/Users/yiwen/Desktop/UHN/Resample-loop.py')


import vtk

inter=vtk.vtkImageInterpolator()
inter.SetInterpolationModeToCubic()

for num in range(0,10):

 filename ="/Users/yiwen/Desktop/Testing-PDT/L9PRE/t1w_0"+str(num)+".dcm"
 reader=vtk.vtkDICOMReader()
 reader.SetFileName(filename)
 reader.Update()
 image = reader.GetOutputPort()

 resample=vtk.vtkImageResample()
 resample.SetInterpolator(inter)
 resample.SetInputConnection(image)
 resample.SetAxisOutputSpacing(0,0.05)
 resample.SetAxisOutputSpacing(1,0.05)



 writer=vtk.vtkDICOMWriter()
 writer.SetInputConnection(resample.GetOutputPort())
 writer.SetFileName(str(0)+str(num)+'.dcm')
 writer.Update()
 writer.Write()



for num in range(10,18):

 filename ="/Users/yiwen/Desktop/Testing-PDT/L9PRE/t1w_"+str(num)+".dcm"
 reader=vtk.vtkDICOMReader()
 reader.SetFileName(filename)
 reader.Update()
 image = reader.GetOutputPort()

 resample=vtk.vtkImageResample()
 resample.SetInterpolator(inter)
 resample.SetInputConnection(image)
 resample.SetAxisOutputSpacing(0,0.05)
 resample.SetAxisOutputSpacing(1,0.05)


 writer=vtk.vtkDICOMWriter()
 writer.SetInputConnection(resample.GetOutputPort())
 writer.SetFileName(str(num)+'.dcm')
 writer.Update()
 writer.Write()

