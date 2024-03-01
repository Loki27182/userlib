clear

a = [0.000, 79.928317; 0.020, 80.348317; 0.040, 80.769983; 0.060, 81.191649; 0.080, 81.614982; 0.100, 82.034982; 0.120, 82.459982; 0.139, 82.883315; 0.159, 83.306648; 0.179, 83.739981; 0.199, 84.173314; 0.249, 85.275000; 0.299, 86.388333; 0.349, 87.485000; 0.401, 88.613333; 0.45, 89.673333; 0.50, 90.738333; 0.60, 92.833333; 0.70, 94.903333; 0.80, 96.961666; 0.901, 99.053333; 0.999, 101.036666; 0.000, 79.926666; -0.020, 79.503333; -0.040, 79.081666; -0.060, 78.658333; -0.079, 78.238333; -0.099, 77.813333; -0.119, 77.388333; -0.139, 76.963333; -0.159, 76.538332; -0.179, 76.113332; -0.199, 75.681665; -0.249, 74.596665; -0.299, 73.488331; -0.349, 72.351665; -0.401, 71.149998; -0.45, 69.961665; -0.50, 68.731665; -0.60, 66.146665; -0.701, 63.481665; -0.80, 60.694998; -0.90, 57.661665; -0.999, 54.449998; 0.000, 79.921666];

v = a(:,1);
[v,idx] = sort(v);
f = a(idx,2);

p1 = polyfit(v(abs(v)<.2),f(abs(v)<.2),1);

v_fine = linspace(min(v),max(v),101);
f_fine = polyval(p1,v_fine);
f_fit = polyval(p1,v);

figure(1)
plot(v,f,'x',v_fine,f_fine,'--')
xlabel('AMO Driver VCO Setpoint (V)')
ylabel({'LF AOM', 'Single-Pass Frequency (MHz)'})
title(['Slope at Center = ' num2str(p1(1),'%1.3f') ' $\frac{\mathrm{kHz}}{\mathrm{mV}}$'])
legend('Data','Fit to central region (-0.2V to 0.2V)','location','southeast')
saveas(gcf,'D:/misc/2024/01/08/data_and_fit.png')

figure(2)
plot(v,f-f_fit,'--x')
xlabel('AMO Driver VCO Setpoint (V)')
ylabel({'LF AOM', 'Single-Pass Frequency (MHz)'})
title('Linear Fit Residuals')
saveas(gcf,'D:/misc/2024/01/08/fit_residuals.png')

figure(3)
v_u = unique(v);
f_u = zeros(size(v_u));
for ii = 1:length(unique(v))
    f_u(ii) = mean(f(v==v_u(ii)));
end
dv = (v_u(1:end-1)+v_u(2:end))/2;
df = diff(f_u)./diff(v_u);
plot(dv,df,'x')
xlabel('AMO Driver VCO Setpoint (V)')
ylabel('AMO Driver Response Slope ($\frac{\mathrm{kHz}}{\mathrm{mV}}$)')
saveas(gcf,'D:/misc/2024/01/08/slope.png')