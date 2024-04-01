clear
clc
close all

path = 'D:/misc/2024/03/19/red_power_calibration_mixer_version_amplified/';
if ~exist(path,'dir')
    mkdir(path)
end

V_set = [10.22,10:-.25:0];
P_mon = [2.21,2.21,2.205,2.2,2.19,2.18,2.15,2.09,1.96,1.76,1.49,1.17,.873,.602,.390,.245,.141,.0783,.0445,.0202,.00960,.00420,.00176,.00071,.00028,.000107,.000042,.000017,.000008,.000004,.000002,.000001,.000001,.000001,.000001,.000001,.000001,.000001,.000001,.000001,.000001,.000001];
V_mon = [2.31,2.31,2.31,2.31,2.31,2.3,2.29,2.26,2.21,2.13,2.01,1.87,1.744,1.625,1.532,1.469,1.423,1.395,1.379,1.37,1.361,1.25,.551,.235,.105,.0565,.0372,.0298,.0269,.0257,.0251,.0249,.0248,.0247,.0247,.0247,.0247,.0247,.0247,.0247,.0247,.0247];
P_mon_0 = 0;
V_mon_0 = .0244;

[V_set,idx] = sort(V_set);
P_mon = P_mon(idx)-P_mon_0;
V_mon = V_mon(idx)-V_mon_0;

[xData, yData] = prepareCurveData( P_mon, V_mon );

ft = fittype( 'a*x*heaviside(b-x)+(c*x+b*(a-c))*heaviside(x-b)+d', 'independent', 'x', 'dependent', 'y' );
opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
opts.Display = 'Off';
opts.StartPoint = [290 .005 .4 0];

% Fit model to data.
fit_P_V = fit( xData, yData, ft, opts );
P_fit = logspace(log10(min(P_mon)),log10(max(P_mon)),1000);
V_fit = fit_P_V(P_fit);
n0 = find(V_mon==V_mon(1),1,'last');
n1 = find(V_mon==V_mon(end),1,'first');
V_set_fit = interp1(V_mon(n0:n1),V_set(n0:n1),V_fit,'pchip');

save([path 'red_power_calibration_mixer_version_amplified.mat'],'V_set','P_mon','V_mon','V_set_fit','P_fit','V_fit')


figure(1)
semilogy(V_set,P_mon)
xlabel('Control Signal (V)','FontSize',14)
ylabel('Optical Power (mW)','FontSize',14)
xlim([0,10])
savefig([path 'control_to_power.fig'])
saveas(gcf,[path 'control_to_power.png'])

figure(2)
plot(P_mon,V_mon,'x',P_fit,V_fit)
xlim([0,.1])
xlabel('Optical Power (mW)','FontSize',14)
ylabel('Monitor Signal (V)','FontSize',14)
savefig([path 'power_to_monitor.fig'])
saveas(gcf,[path 'power_to_monitor.png'])

figure(3)
semilogx(P_mon,V_mon,'x',P_fit,V_fit)
xlim([1e-6,2.5])
xlabel('Optical Power (mW)','FontSize',14)
ylabel('Monitor Signal (V)','FontSize',14)
savefig([path 'power_to_monitor_log.fig'])
saveas(gcf,[path 'power_to_monitor_log.png'])

figure(4)
plot(V_set,V_mon,'x',V_set_fit,V_fit,'--')
xlabel('Control Signal (V)','FontSize',14)
ylabel('Monitor Signal (V)','FontSize',14)
savefig([path 'control_to_monitor.fig'])
saveas(gcf,[path 'control_to_monitor.png'])

figure(5)
semilogy(V_set_fit,V_fit)
xlabel('Control Signal (V)','FontSize',14)
ylabel('Monitor Signal (V)','FontSize',14)
savefig([path 'control_to_monitor_log.fig'])
saveas(gcf,[path 'control_to_monitor_log.png'])

figure(6)
semilogy(V_set_fit(1:end-1)+diff(V_set_fit),smooth(diff(V_fit)./diff(V_set_fit),50))
xlabel('Control Signal (V)','FontSize',14)
ylabel('Monitor Signal (V)','FontSize',14)
savefig([path 'control_to_monitor_slope.fig'])
saveas(gcf,[path 'control_to_monitor_slope.png'])

figure(7)
semilogy(V_set,P_mon*6*2/(pi*.6^2)/.003)
xlabel('Control Signal (V)','FontSize',14)
ylabel('Optical Power ($\times\mathrm{I}_\mathrm{sat}$)','FontSize',14)
xlim([0,10])
savefig([path 'control_to_power_isat.fig'])
saveas(gcf,[path 'control_to_power_isat.png'])