f_set = [.01,.02,.05,.1,.2,.5,1,2,5,10,20,50,75,80,85,100,125,150,155,160];
f_meas = [0.009983,0.020333,0.050333,.1,.2,.5,1,2,5,9.999666,19.999395,49.998,74.997,79.997,84.996666,99.995999,124.995,149.994,154.993887,159.993666];
p_meas = -[65.2,47,23.7,10.7,8.2,8,8,8,7.9,8.1,8.5,10,9.8,9.7,9.7,9.8,10.6,11.5,11.6,11.8];
p_spur = -[61,51,43,48,46,45,45,45,45,44,44,54,40,47,46,48,45,46,43,40];

p_f = polyfit(f_set,f_meas,1);
f_fit_x = linspace(min(f_set),max(f_set),200);


p_p = polyfit(f_set,f_meas,1);
f_fit_x = linspace(min(f_set),max(f_set),200);
f_fit_y = polyval(p_f,f_fit_x);
f_fit = polyval(p_f,f_set);

if ~exist('D:/misc/2024/01/09/DDS_calibration/','dir')
    mkdir('D:/misc/2024/01/09/DDS_calibration/')
end

close all
figure(1)
plot(f_set,f_meas,'x',f_fit_x,f_fit_y,'--')
xlabel('Set Frequency (MHz)')
ylabel('Measured Frequency (MHz)')
legend('Data','Linear Fit','location','southeast')
savefig(gcf,'D:/misc/2024/01/09/DDS_calibration/frequency.fig')
saveas(gcf,'D:/misc/2024/01/09/DDS_calibration/frequency.png')

figure(2)
plot(f_set,(f_meas-f_fit)*1000,'--x')
xlabel('Set Frequency (MHz)')
ylabel('Linear Fit Residuals (kHz)')
savefig(gcf,'D:/misc/2024/01/09/DDS_calibration/residuals.fig')
saveas(gcf,'D:/misc/2024/01/09/DDS_calibration/residuals.png')

figure(3)
semilogx(f_set,p_meas,'-')
xlabel('Set Frequency (MHz)')
ylabel('Carrier Power (dBm)')
savefig(gcf,'D:/misc/2024/01/09/DDS_calibration/power.fig')
saveas(gcf,'D:/misc/2024/01/09/DDS_calibration/power.png')

figure(4)
semilogx(f_set,p_spur-p_meas,'-')
xlabel('Set Frequency (MHz)')
ylabel('SFDR (dBc)')
savefig(gcf,'D:/misc/2024/01/09/DDS_calibration/SDFR.fig')
saveas(gcf,'D:/misc/2024/01/09/DDS_calibration/SDFR.png')