clear
clc
clf
runs = 13:30;
lam = 921+[68230,69001,69502,70003,70506,71004,71500,72000,72501,73000,73500,74001,74503,75004,75500,76004,76500,77002]/100000;
dv = zeros(1,length(runs));
b = zeros(1,length(runs));
gof = zeros(2,length(runs));

lam0 = 1/(10849.304)/100*1e9;

for ii = 1:length(runs)
[dv_i,b_i,gof_i] = analyze_shot(runs(ii));
dv(ii) = dv_i;
b(ii) = b_i;
gof(:,ii) = gof_i';
end
subplot(3,1,1)
plot(lam,b,[lam0,lam0],[-10,10],'--k','LineWidth',2)
xlabel('Vacuum wavelength (nm)','FontSize',14)
ylabel('Broadening Factor','FontSize',14)
ylim([1,1.25])
xlim([min(lam),max(lam)])

subplot(3,1,2)
plot(lam,dv*1000,[lam0,lam0],[-100,100],'--k','LineWidth',2)
xlabel('Vacuum wavelength (nm)','FontSize',14)
% xlabel('Freq (THz)','FontSize',14)
ylabel('Peak separation (mV)','FontSize',14)
ylim([0,60])

subplot(3,1,3)
plot(lam,gof,[lam0,lam0],[-10,10],'--k','LineWidth',2)
xlabel('Vacuum wavelength (nm)','FontSize',14)
ylabel('Adjusted R-squared for Fits','FontSize',14)
legend('Upward Ramp','Downward Ramp')
ylim([.5,1])


filePath = 'D:\misc\2024\05\24\water_line_crap_all';
saveas(gcf,[filePath '.png'])
% savefig([filePath '.fig'])
fid = gcf;
fid.Units = 'Inches';
fid.PaperSize = fid.InnerPosition(3:4);
print([filePath '.pdf'],'-dpdf')
print([filePath '.emf'],'-dmeta')


function [peak_seperation,peak_broadening,gof] = analyze_shot(run_number)
datapath = 'D:\misc\2024\05\24\';

ic_smooth = 3;
t_ramp_max = 0.017;
t_ramp_end = 0.067;

run_str = num2str(run_number,'%04d');
ch1 = readmatrix([datapath 'ALL' run_str '\F' run_str 'CH1.CSV']);
ch3 = readmatrix([datapath 'ALL' run_str '\F' run_str 'CH3.CSV']);
t = ch1(:,4);
v_ic = ch1(:,5);
v_ramp = ch3(:,5);

t_up = t(t<t_ramp_max);
t_dn = t(t>t_ramp_max&t<t_ramp_end);

v_ramp_up = v_ramp(t<t_ramp_max);
v_ramp_dn = v_ramp(t>t_ramp_max&t<t_ramp_end);

p_ramp_up = polyfit(t_up,v_ramp_up,1);
p_ramp_dn = polyfit(t_dn,v_ramp_dn,1);

v_ramp_fit_up = polyval(p_ramp_up,t_up);
v_ramp_fit_dn = polyval(p_ramp_dn,t_dn);

v_ic_up = smooth(v_ic(t<t_ramp_max),ic_smooth);
v_ic_dn = smooth(v_ic(t>t_ramp_max&t<t_ramp_end),ic_smooth);

[fitresult_up,gof_up] = lorentzian_fit(v_ramp_fit_up,v_ic_up);
[fitresult_dn,gof_dn] = lorentzian_fit(v_ramp_fit_dn,v_ic_dn);

peak_seperation = abs(fitresult_dn.b - fitresult_up.b);
peak_broadening = max([fitresult_dn.b,fitresult_up.b])/min([fitresult_dn.b,fitresult_up.b]);
gof = [gof_up.adjrsquare,gof_dn.adjrsquare];
end


function [fitresult,gof] = lorentzian_fit(xData,yData)
[xData,idx] = sort(xData);
yData = yData(idx);
[xData, yData] = prepareCurveData( xData, yData );
[peak_value, peak_location, peak_width, peak_height] = ...
    findpeaks(yData,xData,'NPeaks',1,'SortStr','descend');

ft = fittype( 'a/(((x-b)/c)^2+1)+d', 'independent', 'x', 'dependent', 'y' );
opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
opts.Display = 'Off';
opts.StartPoint = [peak_height, peak_location, peak_width/2, peak_value-peak_height];
[fitresult, gof] = fit( xData, yData, ft, opts );
end