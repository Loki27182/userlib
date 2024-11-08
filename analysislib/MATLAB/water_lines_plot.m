clear
clc
load water_spectroscopic_data.mat

n_bad = 728;

semilogy(transitions.wavelength*1e9,transitions.strength,'x',...
    transitions.wavelength(n_bad)*1e9,transitions.strength(n_bad),'or',...
    'MarkerSize',10,'LineWidth',1.5)
ylim([1e-24,4e-23])
xlabel('Wavelength (nm)','FontSize',14)
ylabel('Transition strength','FontSize',14)

filePath = 'D:\misc\2024\05\30\water_lines';
saveas(gcf,[filePath '.png'])
% savefig([filePath '.fig'])
fid = gcf;
fid.Units = 'Inches';
fid.PaperSize = fid.InnerPosition(3:4);
print([filePath '.pdf'],'-dpdf')
print([filePath '.emf'],'-dmeta')