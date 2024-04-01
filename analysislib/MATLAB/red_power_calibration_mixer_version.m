clear

path = 'D:/misc/2024/03/18/red_power_calibration_mixer_version/';
if ~exist(path,'dir')
    mkdir(path)
end

V = [0,1.99,2.189,2.389,2.605,3.001,3.201,3.4,3.604,3.8,4.003,4.201,4.401,4.602,4.8,5.001,5.219,5.421,5.618,5.820,6.015,6.218,6.415,6.62,6.82,7.03,7.22,7.43,7.62,7.83,8.03,8.22,8.42,8.62,8.82,9.02,9.22,9.42,9.63,9.82,10.03];
P_mW = [[0,0,0,0,1,2,4,8,16,34,73,155,355,710]/1e6,[1.46,2.94,5.97,11.2,20.2,35.2,58.2,94.8,150,229,332,465,626,811]/1e3,[1.01,1.21,1.38,1.51,1.58,1.63,1.67,1.68,1.69,1.70,1.71,1.71,1.71]];

save([path 'red_power_calibration_mixer_version.mat'],'V','P_mW')

figure(1)
% subplot(2,1,1)
plot(V,P_mW)
xlabel('Control Signal (V)','FontSize',14)
ylabel('Output Power (mW)','FontSize',14)
xlim([0,10])
savefig([path 'control_to_power.fig'])
saveas(gcf,[path 'control_to_power.png'])

figure(2)
% subplot(2,1,2)
semilogy(V,P_mW)
xlabel('Control Signal (V)','FontSize',14)
ylabel('Output Power (mW)','FontSize',14)
xlim([0,10])
ylim([5e-7,2e0])
savefig([path 'control_to_power_log.fig'])
saveas(gcf,[path 'control_to_power_log.png'])