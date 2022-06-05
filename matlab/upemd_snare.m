%uiopen('C:\Users\Caléo\Desktop\UPEMD\632743__noillox__snares98bpm-loop.wav',1)
x = (data(:,1) + data(:,2))/2;
x = x';
x = x(1:fs*3);
numSift = 10; %default 10, for duffing numSift=2000
numPhase = 16; % only for speedMode=2; otherwise this parameter is useless
numImf = 10;
ampSin = 0.4;
[imf] = upemd_ver_1_1(x,1,numImf,numSift,numPhase,ampSin); 
