clear
clc
clf
close all
lam0 = 1/(10849.304)/100*1e9;

name = 'cavity_asymmetry';
savefig = true;
runs = 1:30;
titles = {{'$I_{\mathrm{TA}} = 980$ mA$\rightarrow P_{922} = 250$ mW','$\lambda = 921.725$ nm$, t_{\mathrm{ramp}} = 5$ s'},...
    {'$I_{\mathrm{TA}} = 700$ mA$\rightarrow P_{922} = 110$ mW','$\lambda = 921.725$ nm$, t_{\mathrm{ramp}} = 5$ s'},...
    {'$I_{\mathrm{TA}} = 1200$ mA$\rightarrow P_{922} = 300$ mW','$\lambda = 921.725$ nm$, t_{\mathrm{ramp}} = 5$ s'},...
    {'$I_{\mathrm{TA}} = 1200$ mA$\rightarrow P_{922} = 300$ mW','$\lambda = 921.725$ nm$, t_{\mathrm{ramp}} = 2.5$ s'},...
    {'$I_{\mathrm{TA}} = 1200$ mA$\rightarrow P_{922} = 300$ mW','$\lambda = 921.725$ nm$, t_{\mathrm{ramp}} = 50$ ms'},...
    {'$I_{\mathrm{TA}} = 2470$ mA$\rightarrow P_{922} = 1000$ mW','$\lambda = 921.725$ nm$, t_{\mathrm{ramp}} = 50$ ms'},...
    {'Bad data - ignore'},...
    {'Bad data - ignore'},...
    {'Bad data - ignore'},...
    {'Bad data - ignore'},...
    {'Bad data - ignore'},...
    {'Bad data - ignore'},...
    {'$I_{\mathrm{TA}} = 1680$ mA$\rightarrow P_{922} = 500$ mW','$\lambda = 921.68230$ nm$, t_{\mathrm{ramp}} = 50$ ms'},...
    {'$I_{\mathrm{TA}} = 1680$ mA$\rightarrow P_{922} = 500$ mW','$\lambda = 921.69001$ nm$, t_{\mathrm{ramp}} = 50$ ms'},...
    {'$I_{\mathrm{TA}} = 1680$ mA$\rightarrow P_{922} = 500$ mW','$\lambda = 921.69502$ nm$, t_{\mathrm{ramp}} = 50$ ms'},...
    {'$I_{\mathrm{TA}} = 1680$ mA$\rightarrow P_{922} = 500$ mW','$\lambda = 921.70003$ nm$, t_{\mathrm{ramp}} = 50$ ms'},...
    {'$I_{\mathrm{TA}} = 1680$ mA$\rightarrow P_{922} = 500$ mW','$\lambda = 921.70506$ nm$, t_{\mathrm{ramp}} = 50$ ms'},...
    {'$I_{\mathrm{TA}} = 1680$ mA$\rightarrow P_{922} = 500$ mW','$\lambda = 921.71004$ nm$, t_{\mathrm{ramp}} = 50$ ms'},...
    {'$I_{\mathrm{TA}} = 1680$ mA$\rightarrow P_{922} = 500$ mW','$\lambda = 921.71500$ nm$, t_{\mathrm{ramp}} = 50$ ms'},...
    {'$I_{\mathrm{TA}} = 1680$ mA$\rightarrow P_{922} = 500$ mW','$\lambda = 921.72000$ nm$, t_{\mathrm{ramp}} = 50$ ms'},...
    {'$I_{\mathrm{TA}} = 1680$ mA$\rightarrow P_{922} = 500$ mW','$\lambda = 921.72501$ nm$, t_{\mathrm{ramp}} = 50$ ms'},...
    {'$I_{\mathrm{TA}} = 1680$ mA$\rightarrow P_{922} = 500$ mW','$\lambda = 921.73000$ nm$, t_{\mathrm{ramp}} = 50$ ms'},...
    {'$I_{\mathrm{TA}} = 1680$ mA$\rightarrow P_{922} = 500$ mW','$\lambda = 921.73500$ nm$, t_{\mathrm{ramp}} = 50$ ms'},...
    {'$I_{\mathrm{TA}} = 1680$ mA$\rightarrow P_{922} = 500$ mW','$\lambda = 921.74001$ nm$, t_{\mathrm{ramp}} = 50$ ms'},...
    {'$I_{\mathrm{TA}} = 1680$ mA$\rightarrow P_{922} = 500$ mW','$\lambda = 921.74503$ nm$, t_{\mathrm{ramp}} = 50$ ms'},...
    {'$I_{\mathrm{TA}} = 1680$ mA$\rightarrow P_{922} = 500$ mW','$\lambda = 921.75004$ nm$, t_{\mathrm{ramp}} = 50$ ms'},...
    {'$I_{\mathrm{TA}} = 1680$ mA$\rightarrow P_{922} = 500$ mW','$\lambda = 921.75500$ nm$, t_{\mathrm{ramp}} = 50$ ms'},...
    {'$I_{\mathrm{TA}} = 1680$ mA$\rightarrow P_{922} = 500$ mW','$\lambda = 921.76004$ nm$, t_{\mathrm{ramp}} = 50$ ms'},...
    {'$I_{\mathrm{TA}} = 1680$ mA$\rightarrow P_{922} = 500$ mW','$\lambda = 921.76500$ nm$, t_{\mathrm{ramp}} = 50$ ms'},...
    {'$I_{\mathrm{TA}} = 1680$ mA$\rightarrow P_{922} = 500$ mW','$\lambda = 921.77002$ nm$, t_{\mathrm{ramp}} = 50$ ms'}};

for ii = 1:length(runs)
run = ii;

[dv,b,gof,v_ramp_fit_up,v_ramp_fit_dn,v_ic_up,v_ic_dn,t,v_ic,v_ramp] = analyze_shot(run);
% figure(ii)
clf
% subplot(2,1,1)
plot(v_ramp_fit_up,v_ic_up,v_ramp_fit_dn,v_ic_dn,'LineWidth',2)
xlabel('PO frequency (arb)','FontSize',14)
ylabel('Intracavity power (arb)','FontSize',14)
if ii <= length(titles)
title(titles{ii},'FontSize',16)
end
drawnow

% subplot(2,1,2)
% plot(t,v_ic,t,v_ramp)

if savefig
filePath = ['D:\misc\2024\05\24\' name '_' num2str(ii,'%02d')];
saveas(gcf,[filePath '.png'])
% savefig([filePath '.fig'])
fid = gcf;
fid.Units = 'Inches';
fid.PaperSize = fid.InnerPosition(3:4);
print([filePath '.pdf'],'-dpdf')
print([filePath '.emf'],'-dmeta')
end
end

function [peak_seperation,peak_broadening,gof,v_ramp_fit_up,v_ramp_fit_dn,v_ic_up,v_ic_dn,t,v_ic,v_ramp] = analyze_shot(run_number)
datapath = 'D:\misc\2024\05\24\';

ic_smooth = 3;
t_ramp_max = 0.017;
t_ramp_end = 0.067;

run_str = num2str(run_number,'%04d');
ch1 = readmatrix([datapath 'ALL' run_str '\F' run_str 'CH1.CSV']);
ch3 = readmatrix([datapath 'ALL' run_str '\F' run_str 'CH3.CSV']);
t = ch1(:,4);
t = t - t(1);
t_norm = max(t);
% t = t/t_norm;
% min(t)
% max(t)
t_ramp_max = 0.45;
t_ramp_end = 0.067;

v_ic = ch1(:,5);
v_ramp = ch3(:,5);
mask_up = 0.05<t/t_norm & t/t_norm<.45;
mask_down = 0.55<t/t_norm & t/t_norm<.95;



t_up = t(mask_up);
t_dn = t(mask_down);

v_ramp_up = v_ramp(mask_up);
v_ramp_dn = v_ramp(mask_down);

p_ramp_up = polyfit(t_up,v_ramp_up,1);
p_ramp_dn = polyfit(t_dn,v_ramp_dn,1);

v_ramp_fit_up = polyval(p_ramp_up,t_up);
v_ramp_fit_dn = polyval(p_ramp_dn,t_dn);

v_ic_up = smooth(v_ic(mask_up),ic_smooth);
v_ic_dn = smooth(v_ic(mask_down),ic_smooth);

% size(v_ramp_fit_up)
% size(v_ramp_fit_dn)
% size(v_ic_up)
% size(v_ic_dn)

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