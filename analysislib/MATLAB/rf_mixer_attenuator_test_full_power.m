V = [0:.1:1,2:1:10];
P = -[43.3,43.05,41.93,40.45,38.88,37.40,35.99,34.78,33.66,32.6,31.63,24.43,19.18,14.70,10.71,7.4,4.65,2.29,0.23,-.96];

semilogx(V,P,'-x','LineWidth',1.5)
xlabel('Control Signal (V)','FontSize',14)
ylabel('RF Power (dBm)','FontSize',14)
xticklabels({'100 mV','1.00V','10.00V'})
filePath = 'D:\misc\2024\05\20\mixer_attenuator_all';
saveas(gcf,[filePath '.png'])
savefig([filePath 'fig'])