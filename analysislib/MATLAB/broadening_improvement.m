clear
clc
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% For tomorrow's data, the scan range was changed from 0.6 to 0.5 V %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
[l,v,w,datapath] = getData('2024/05/30',[5,8,1]);

savefig = true;
name = 'broadening_improvement_day_1';
titles = {'5/29/2024 Early Afternoon','5/29/2024 Late Afternoon (after changing temp)','5/30/2024 9:30AM'};
clf
for ii = 1:3
% subplot(1,3,ii)
figure(ii)
clf
l_plot = l{ii};
v_plot = 25*v{ii};
l_FWHM = [min(l_plot(v_plot>max(v_plot)/2)),max(l_plot(v_plot>max(v_plot)/2))];
v_FWHM = max(v_plot)/2*[1,1];

plot(l_plot,v_plot,'-',l_FWHM,v_FWHM,':r','LineWidth',2)
xlabel('Cavity length (arb)','FontSize',14)
ylabel('Intracavity power (arb)','FontSize',14)
xlim([-.1,1.1])
ylim([-.05,1.2])
title({titles{ii},['$FWHM = ' num2str(w(ii),'%0.3f') '$']},'FontSize',16)

if savefig
filePath = [datapath name '_' num2str(ii,'%01d')];
saveas(gcf,[filePath '.png'])
% savefig([filePath '.fig'])
fid = gcf;
fid.Units = 'Inches';
fid.PaperSize = fid.InnerPosition(3:4);
print([filePath '.pdf'],'-dpdf')
print([filePath '.emf'],'-dmeta')
end

end



function [l,v,w,datapath] = getData(date,used_channels)
n_sm = 10;
datapath = ['D:\misc\' num2str(date(1:4),'%04d') '\' num2str(date(6:7),'%02d') '\' num2str(date(9:10),'%02d') '\'];
channels = {'F0000CH1','F0000CH2','F0000CH3','F0000CH4','F0000RFA','F0000RFB','F0000RFC','F0000RFD'};
for ii = 1:length(used_channels)
ch = readmatrix([datapath channels{used_channels(ii)} '.CSV']);
ti = ch(50:end-50,4);
t{ii} = 1 - (ti - min(ti))/(max(ti)-min(ti));
% t{ii} = 1-(ch(50:end-50,4)-ch(1,4))/(ch(end,4)-ch(1,4));
vi = ch(50:end-50,5);
v_norm = (max(vi)-min(vi));
v{ii} = vi/v_norm;
% v{ii} = (ch(:,5)-min(ch(:,5)))/(max(ch(:,5))-min(ch(:,5)));%[ch1(:,5)/max(ch1(:,5)), ch2(:,5)/max(ch2(:,5)), ch3(:,5)/max(ch3(:,5)),cha(:,5)/max(cha(:,5)),chd(:,5)/max(chd(:,5))];
l_plot = t{ii};
v_plot = v{ii};

v_plot_sm = smooth(v_plot,n_sm);
dv_plot = diff(v_plot_sm);
dv_plot = dv_plot/max(abs(dv_plot));
% dl_plot = l_plot(1:end-1)+mean(diff(l_plot)/2);

% size(l_plot(find(abs(dv_plot)==max(abs(dv_plot)),1)))
l_plot = l_plot - l_plot(find(abs(dv_plot)==max(abs(dv_plot)),1));
v{ii} = v_plot(abs(l_plot)<=.055);
l{ii} = l_plot(abs(l_plot)<=.055)*20;
w(ii) = max(l{ii}(v{ii}>.5)) - min(l{ii}(v{ii}>.5));
v{ii} = v{ii}*v_norm;
end

end