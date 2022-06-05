upemd_snare
subplot(11,1,1)
plot(x(1,:))
for i = 1:11
    figure(1)
    subplot(11,1,i+1)
    plot(imf(i,:))
    
end