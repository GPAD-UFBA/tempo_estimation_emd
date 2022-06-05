function [y] = downmix(x)
    [m, n] = size(x);
    if n == 2
        y = sum(x,2);
        peakAmp = max(abs(y));
        y = y/peakAmp;
                
        %  check the L/R channels for orig. peak Amplitudes
        peakL = max(abs(x(:, 1)));
        peakR = max(abs(x(:, 2))); 
        maxPeak = max([peakL peakR]);
        y = y*maxPeak;
     else
        y=x;
     end
end

