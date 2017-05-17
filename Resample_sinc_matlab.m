% The number of slices of the dicom file
nFrames = 18; 

% Set the number of rows and columns 
new_dimension = 512;
old_dimension = 128;

% Create a matrix to store the pixel value from the original dicom file.
X = repmat(uint16(0), [old_dimension old_dimension 1 nFrames]);

for p=1:nFrames
    % Read the original dicom file
    fname = sprintf('t1w_%02d.dcm',p-1);
    X(:,:,1,p) = dicomread(fname);      
end

% Get the information from the original dicom(any slice) 
info = dicominfo('t1w_00.dcm');
% Modify some of the image data to fit the new(resampled) dicom image
info.Rows = new_dimension;
info.Columns = new_dimension;
info.Height = new_dimension;
info.Width = new_dimension;
% Calculate new pixel spacing based on the original spacing and number of
% new rows/columns. In this example, the original pixel spacing is 0.2. Row
% number is increased by 4, so the new spacing should be reduced by 4.
% 0.2/4=0.05
info.PixelSpacing = [0.05 0.05]; 
info.AcquisitionMatrix= [0;new_dimension;new_dimension*2;0];
%info.NumberOfPhaseEncodingSteps = new_dimension;



% Create a new matrix with new dimension and values 0, this is an example
% of increasing resolution by 4
resliced_dicom = repmat(uint16(0), [new_dimension new_dimension 1 nFrames]);
for m = 1:18
    for i=1:old_dimension
        for j=1:old_dimension
           resliced_dicom(4*i-3,4*j-3,1,m)= X(i,j,1,m);
           resliced_dicom(4*i-2,4*j-3,1,m)= X(i,j,1,m);
           resliced_dicom(4*i-1,4*j-3,1,m)= X(i,j,1,m);
           resliced_dicom(4*i,4*j-3,1,m)= X(i,j,1,m);
        
           resliced_dicom(4*i-3,4*j-2,1,m)= X(i,j,1,m);
           resliced_dicom(4*i-2,4*j-2,1,m)= X(i,j,1,m);
           resliced_dicom(4*i-1,4*j-2,1,m)= X(i,j,1,m);
           resliced_dicom(4*i,4*j-2,1,m)= X(i,j,1,m);
        
           resliced_dicom(4*i-3,4*j-1,1,m)= X(i,j,1,m);
           resliced_dicom(4*i-2,4*j-1,1,m)= X(i,j,1,m);
           resliced_dicom(4*i-1,4*j-1,1,m)= X(i,j,1,m);
           resliced_dicom(4*i,4*j-1,1,m)= X(i,j,1,m);
        
           resliced_dicom(4*i-3,4*j,1,m)= X(i,j,1,m);
           resliced_dicom(4*i-2,4*j,1,m)= X(i,j,1,m);
           resliced_dicom(4*i-1,4*j,1,m)= X(i,j,1,m);
           resliced_dicom(4*i,4*j,1,m)= X(i,j,1,m);
        end
    end
end


                      

% Create the kernel
k_dimension = 5; %use odd number
K = zeros([k_dimension k_dimension 1 k_dimension]);
center = (k_dimension +1)/2;
kernel_weight = 0;

for i=1:k_dimension
    for j=1:k_dimension
        for k=1:k_dimension
            K(i,j,1,k)= sinc3d(abs(i-center),abs(j-center),abs(k-center));
            kernel_weight = kernel_weight + K(i,j,1,k);
            
        end
    end
end

Kernel = K/kernel_weight;

% Convolution
Resampled_dicom = convn(resliced_dicom,Kernel,'same');
% IMPORTANT! Convert the pixel value from double to integer.  
Resampled_dicom_to_int = uint16(floor(Resampled_dicom));

% Write the new dicom
frame = Resampled_dicom_to_int;
filename = '5PRE_sinc_resampled_5x5_0.5.dcm';
dicomwrite(frame, filename,info,'CreateMode','Copy')

    
function output= sinc3d(x,y,z)

    output = (sinc(x+0.5)^2 + sinc(y+0.5)^2 + sinc(z+0.5)^2)^0.5;

end

