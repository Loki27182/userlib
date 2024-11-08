a = readtable("isolator_magnetometer_data.csv");
t = a.t_s_;
Bz = a.B_z_mG_;

B_max = mean(Bz(t>8.2&t<9.2));
B_min = mean(Bz(t>10.2&t<11));

plot(t,Bz,'.',t,smooth(Bz,10),'--',t,ones(size(t))*B_max,'--k',t,ones(size(t))*B_min,'--k')
xlabel('Time (s)','FontSize',14)
ylabel('$B_Z$ (mG)','FontSize',14)
title(['$\Delta B_Z/2 = ' num2str((B_max-B_min)/2,'%0.1f') '$ mG'],'FontSize',16)

filePath = 'D:\misc\2024\05\14\isolator_data_1meter';
saveas(gcf,[filePath '.png'])
savefig([filePath 'fig'])