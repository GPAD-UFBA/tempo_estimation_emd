clc,clear
datasets_list = dir('D:\Banco de Dados GPAD\dataset');
datasets_list_length = length(datasets_list);
new_Fs = 11025;
mkdir h5files



startMode = 0;
numSift = 10;
numPhase = 8; 
numImf = 15;
ampSin = 0.5;


sample_rate = 1000;
seconds = 10;
num_samples = sample_rate*seconds;
time_vect = linspace(0, seconds, num_samples);

x = cos(2 * pi * 1 * time_vect);
x = x + sin(2 * pi * 2.2e-1 * time_vect)  ;
[imf] = upemd_ver_1_1(x,startMode,numImf,numSift,numPhase,ampSin);
imf = imf';
plot(imf)
% for i=3:3
%     path = strcat(datasets_list(i).folder,'\', datasets_list(i).name);
%     dataset_files = dir(fullfile(path, '**\*.*'));
%     dataset_files = dataset_files(~[dataset_files.isdir]);
%     files_length = length(dataset_files);
%     
%     for j=1:files_length
%         [fPath, fName, fExt] = fileparts(dataset_files(j).name);
% 
%         if strcmp(fExt,'.wav') || strcmp(fExt,'.mp3')
%             sAudioFile = strcat(dataset_files(j).folder,'\',dataset_files(j).name);
%             [x,Fs] = audioread(sAudioFile); 
%             y = downmix(x);
%             y_resamp = resample(x,new_Fs,Fs)';
%             
%             dataset_name = strcat('/',fName);
%             [imf] = upemd_ver_1_1(y_resamp,startMode,numImf,numSift,numPhase,ampSin);
%             sImf = size(imf,2);
%             file_name = strcat('h5files/',datasets_list(i).name,'.h5');
%             file_name
%             dataset_name
%             
%             h5create(file_name,dataset_name,[numImf sImf])
%             h5write(file_name,dataset_name, imf)
% 
%         end
%         
%         
%     end 
% end    
