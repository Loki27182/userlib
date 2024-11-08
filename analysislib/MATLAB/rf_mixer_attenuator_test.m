P0 = 1.23;
V = -10:.5:10;
V2 = -2:.1:2;
V3 = -.1:.01:.1;
P3 = -[41.55,42.0,42.4,42.83,43.2,43.55,43.87,44.1,44.23,44.3,44.3,...
    44.1,43.93,43.67,43.35,42.95,42.58,42.14,41.71,41.23,40.8];
P2 = -[17.18,17.71,18.26,18.82,19.42,20.08,20.75,21.46,22.22,23.03,23.93,24.9,25.97,27.17,28.52,30.1,32.0,34.35,37.45,41.6,44.35,...
    40.7,36.7,33.75,31.5,29.7,28.15,26.83,25.65,24.6,23.64,22.77,21.95,21.2,20.48,19.81,19.16,18.56,18.00,17.45,16.91];
P = -[.76,1.0,1.51,2.17,2.86,3.57,4.3,5.06,5.87,6.74,7.71,8.79,10.02,11.42,13.04,14.95,17.25,20.14,24.01,30.18,44.5,...
    29.88,23.84,20.01,17.12,14.81,12.9,11.28,9.88,8.67,7.59,6.63,5.77,4.97,4.22,3.49,2.78,2.09,1.43,.89,.64];

G_plot = [P,P2,P3]-P0;

V_plot = [V,V2,V3];

V_plot_1 = V_plot(V_plot>0);
V_plot_2 = -V_plot(V_plot<0);
G_plot_1 = G_plot(V_plot>0);
G_plot_2 = G_plot(V_plot<0);

[V_plot_1,idx] = sort(V_plot_1);
G_plot_1 = G_plot_1(idx);
[V_plot_2,idx2] = sort(V_plot_2);
G_plot_2 = G_plot_2(idx2);

subplot(1,2,1)
semilogx(V_plot_1,G_plot_1,'-x',V_plot_2,G_plot_2,'-x','LineWidth',1.5)
xlabel('Control Signal (V)','FontSize',14)
ylabel('RF Power (dBm)','FontSize',14)
xticklabels({'10 mV','100 mV','1.00V','10.00V'})
legend({'Positive Control Signal','Negative Control Signal'},'Location','northwest','FontSize',12)

subplot(1,2,2)
plot(V_plot_1,10.^(G_plot_1/10),'-x',V_plot_2,10.^(G_plot_2/10),'-x','LineWidth',1.5)
xlabel('Control Signal (V)','FontSize',14)
ylabel('RF Power (fraction)','FontSize',14)
legend({'Positive Control Signal','Negative Control Signal'},'Location','northwest','FontSize',12)

filePath = 'D:\misc\2024\05\16\mixer_attenuator_data_ZX05-1MHZ-S';
saveas(gcf,[filePath '.png'])
savefig([filePath 'fig'])