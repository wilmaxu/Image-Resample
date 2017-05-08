#execfile('/Users/yiwen/Desktop/UHN/ResampleNew.py')

import vtk

filename ="/Users/yiwen/Desktop/tumor_brain/9post.nii"
reader=vtk.vtkNIFTIReader()

reader.SetFileName(filename)
reader.Update()

header=vtk.vtkNIFTIHeader()
header=reader.GetNIFTIHeader()

image = reader.GetOutputPort()


inter=vtk.vtkImageInterpolator()
inter.SetInterpolationModeToCubic()

resample=vtk.vtkImageResample()
resample.SetInterpolator(inter)
resample.SetInterpolationModeToCubic()
resample.SetInputConnection(image)
resample.SetAxisOutputSpacing(0,0.0497)
resample.SetAxisOutputSpacing(1,0.0497)
resample.SetAxisOutputSpacing(2,0.25)


writer=vtk.vtkNIFTIWriter()
writer.SetFileName('tumor_9post.nii')
writer.SetInputConnection(resample.GetOutputPort())
writer.SetNIFTIHeader(header)
writer.Update()
writer.Write()

