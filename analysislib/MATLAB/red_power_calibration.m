clear
clc
close all

I_sat = .003;
r = 0.6;
n_resp = 200;

n_sm = 10;
n_sm_2 = 30;
t_cutoff = [-9.4,3.5;2.8,10.29];
path = 'D:/misc/2024/03/15/red_power_calibration/';

for n = 1:2
    for m = 1:3
        a = readmatrix(['D:/misc/2024/03/15/red_power_calibration/ALL' ...
            num2str(n-1,'%04d') '/F' num2str(n-1,'%04d') 'CH' num2str(m,'%1d') '.csv'],...
            'Range',[1,4]);
        mask = a(:,1)>t_cutoff(n,1) & a(:,1)<t_cutoff(n,2);
        t{n} = a(mask,1);
        V{n}(:,m) = smooth(a(mask,2),n_sm);
    end
end
t{1} = t{1} - t{1}(1);
t{2} = t{2} - t{2}(1);

% plot(t{1},V{1}(:,1),t{1},V{1}(:,2),t{1},V{1}(:,3))

V_cont_0 = [V{1}(:,1)];
V_cont_1 = [V{2}(:,1)];
P_opt_0 = [V{1}(:,2)]/2*7.8;
P_opt_1 = [V{2}(:,2)]/2*7.8;
V_mon_0 = [V{1}(:,3)];
V_mon_1 = [V{2}(:,3)];

mask = P_opt_0>max(P_opt_1);

V_cont = [V_cont_0(mask)',V_cont_1'];
P_opt = [P_opt_0(mask)',P_opt_1'];
V_mon = [V_mon_0(mask)',V_mon_1'];

[V_cont_0,idx] = sort(V_cont);
P_opt_0 = P_opt(idx);
V_mon_0 = V_mon(idx);

V_cont_1 = unique(V_cont_0);
P_opt_1 = zeros(size(V_cont_1));
V_mon = zeros(size(V_cont_1));
for ii = 1:length(V_cont_1)
    P_opt_1(ii) = mean(P_opt_0(V_cont_0==V_cont_1(ii)));
    V_mon_1(ii) = mean(V_mon_0(V_cont_0==V_cont_1(ii)));
end

V_cont = linspace(min(V_cont),3.726,n_resp);
P_opt = interp1(V_cont_1,P_opt_1,V_cont);
V_mon = interp1(V_cont_1,V_mon_1,V_cont);

V1 = [0,1:.5:3.5,3.726];
P_rf_dBm = [-24.8,-21.2,-19.2,-17,-14.5,-11.25,-6.6,-3.8]+30;
P_rf_dBm = interp1(V1,P_rf_dBm,V_cont,'makima');
P_rf_W = 10.^(P_rf_dBm/10)/1000;

figure(1)
plot(P_rf_W,P_opt,'x')

R_high = 100000;
R_low = 100000/10;


%%
% subplot(2,2,2)
figure(2)
plot(t{2}(:,1),V{2}(:,1),t{2},V{2}(:,2)/2*7.8,t{2},V{2}(:,3))
xlabel('Time (s)','FontSize',14)
ylabel('Voltage (V)/Power (mW)','FontSize',14)
xlim([0,max(t{2})])
legend('Control Signal (zoomed)','Power per beam (zoomed)',...
    'Monitor Signal(zoomed)',...
    'location','northwest','FontSize',10)
% savefig([path 'raw_data_zoomed.fig'])
% saveas(gcf,[path 'raw_data_zoomed.png'])

% subplot(2,2,1)
figure(2)
co = colororder;
plot(t{1}(mask),V{1}(mask,1),...
    t{1}(mask),V{1}(mask,2)/2*7.8,...
    t{1}(mask),V{1}(mask,3))
hold on
plot(t{1}(~mask),V{1}(~mask,1),'--',...
    t{1}(~mask),V{1}(~mask,2)/2*7.8,'--'...
    ,t{1}(~mask),V{1}(~mask,3),'--')
hold off
drawnow
fid = gcf;
fid.Children(1).Children(3).Color = co(1,:);
fid.Children(1).Children(2).Color = co(2,:);
fid.Children(1).Children(1).Color = co(3,:);
xlabel('Time (s)','FontSize',14)
ylabel('Voltage (V)','FontSize',14)
xlim([0,max(t{1})])
legend('Control Signal (V)','Power per beam (mW)','Monitor Signal (V)',...
    'Control Signal (ignored in favor of zoomed data)',...
    'Power per beam (ignored in favor of zoomed data)',...
    'Monitor Signal (ignored in favor of zoomed data)',...
    'location','northwest','FontSize',10)
% savefig([path 'raw_data.fig'])
% saveas(gcf,[path 'raw_data.png'])

% subplot(2,3,4)
figure(3)
semilogy(V_cont,smooth(P_opt,n_sm_2)*2*6/(pi*r^2)/I_sat)
xlim([0,max(V_cont)])
xlabel('Control Voltage (V)','FontSize',14)
ylabel('Power ($\times \mathrm{I}_{\mathrm{sat}}$)','FontSize',14)
% savefig([path 'control_to_power_response.fig'])
% saveas(gcf,[path 'control_to_power_response.png'])

% subplot(2,3,5)
figure(4)
plot(V_cont,V_mon)
xlim([0,max(V_cont)])
xlabel('Control (V)','FontSize',14)
ylabel('Monitor Circuit Output (V)','FontSize',14)
% savefig([path 'control_to_monitor_response.fig'])
% saveas(gcf,[path 'control_to_monitor_response.png'])

% subplot(2,3,6)
figure(5)
semilogy(V_cont(1:end-1)+diff(V_cont)/2,...
    smooth(medfilt1(diff(V_mon)./diff(V_cont),n_sm_2),n_sm))
xlim([0,max(V_cont)])
xlabel('Control (V)','FontSize',14)
ylabel(['Monitor Response Slope ($\frac{\mathrm{V}_{\mathrm{mon}}}'...
    '{\mathrm{V}_{\mathrm{cont}}}$)'],'FontSize',14)
% savefig([path 'monitor_slope_response.fig'])
% saveas(gcf,[path 'monitor_slope_response.png'])