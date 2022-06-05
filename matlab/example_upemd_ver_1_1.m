function example_upemd_ver_1_0()
% Example  UPEMD  (Uniform Phase EMD): date 2018-0822
% input parameters:
numSift = 10; %default 10, for duffing numSift=2000
numPhase = 16; % only for speedMode=2; otherwise this parameter is useless
numImf = 10;

i_example = 1;
if (i_example==1) % two-tone signal with intermittency
   ampSin = 0.2; % amplitude of the assisted sinusoids
elseif (i_example==2) % one-tone signal
  ampSin = 0.3; % amplitude of the assisted sinusoids
elseif (i_example==6)
     ampSin = 0.4; % amplitude of the assisted sinusoids  
else % % brain blood flow velocity
    fprintf('Wrong Input !!\n');
   assert(1==0); 
end

[fs,x] = input_signal(i_example);
size(x)

tic;
[imf] = upemd_ver_1_1(x,1,numImf,numSift,numPhase,ampSin); 
toc;

plot_figure_list(11,'UPEMD',imf(:,:));

if (1) % Run Ensemble EMD (EEMD)  
NE = 200; % number of ensemble

tic;
[imf2] = eemd(x,ampSin,NE,numImf,0,numSift,3,1,2,1,1); % EEMD
toc; 

plot_figure_list(12,'EEMD',imf2(:,:));   
end %

if (1) % Run EMD 
tic;
[imf3] = emd(x, 1, 2, numImf, numSift); imf3 = imf3'; 
toc;

plot_figure_list(13,'EMD',imf3(:,:));   
end % 1
    
return; % example_upemd 
   

function [fs,x] = input_signal(i_example) 
if (i_example==1) % two-tone signal with intermittency
  fs = 1;
  t=0:960-1;
  ndata = size(t,2);
  xlow = 1*cos(2*pi/240*t+1);
  xhigh = zeros(1,ndata);
  
  wiggle = 0.1*sin(2*pi*t(1:80)/8);
  n1= 400; n2=  479;
  xhigh(n1:n2)=wiggle;
  x = xlow + xhigh;      
elseif (i_example==2) % one-tone signal
  fs = 1; 
  t=1:1000;
  x = cos(2*pi*t/8);

elseif (i_example==6) % brain blood flow velocity
 fs = 50;
 load -ascii S0305SB_base.BFVL.txt;
 x = S0305SB_base_BFVL; x=x';
 [1];
else
   fprintf('Wrong Input !!\n');
   assert(1==0); 
end
return; % input_signal

function [] = plot_figure_list(fig_num, figTitle, y)
        
numimf = size(y,1);
t1=1;
t2=size(y,2);

sumdy(1) = 0;
for (i=1:numimf-1)
    dy(i) = min(y(i,t1:t2))-max(y(i+1,t1:t2));
    sumdy(i+1) = sumdy(i) + 1.2*dy(i);
end

figure(fig_num);clf; hold on;
for (i=1:numimf)
  plot(y(i,t1:t2)+sumdy(i)-0.1*(i-1),'r','LineWidth',2.0);   
end
title(figTitle);
[1];
return;

    
