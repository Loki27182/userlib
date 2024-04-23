clear
clc

expName = 'quick_trim_sweep';
date = '2024/04/03';
basePath = 'D:/labscript/Experiments/SrMain/';

% run = 10;
% trim_z = 0:.5:5;
% trim_x = 0:.5:5;
% trim_y = trim_x;
% NP1 = 3;
% NP2 = 4;

% run = 11;
% trim_z = 0:.2:2;
% trim_x = 0:.5:5;
% trim_y = trim_x;
% NP1 = 3;
% NP2 = 4;
% 
% run = 12;
% trim_z = linspace(.2,1.4,11);
% trim_x = 0:.5:5;
% trim_y = trim_x;
% NP1 = 3;
% NP2 = 4;
% 
% run = 13;
% trim_z = linspace(.2,1.4,11);
% trim_x = linspace(.05,4.55,10);
% trim_y = trim_x;
% NP1 = 3;
% NP2 = 4;

% run = 15;
% trim_z = 1;
% trim_x = linspace(0,1,11);
% trim_y = linspace(0,3,11);
% NP1 = 1;
% NP2 = 1;

% run = 16;
% trim_z = 1;
% trim_x = linspace(0,5,11);
% trim_y = linspace(0,5,11);
% NP1 = 1;
% NP2 = 1;

% run = 17;
% trim_z = linspace(.2,1.4,11);
% trim_x = linspace(.5,5,10);
% trim_y = linspace(0,4.5,10);
% NP1 = 3;
% NP2 = 4;

% run = 18;
% trim_z = linspace(.2,1.4,11);
% trim_x = linspace(.5,5,10);
% trim_y = linspace(0,4.5,10);
% NP1 = 3;
% NP2 = 4;
% 
% run = 19;
% trim_z = linspace(.2,1.4,11);
% trim_x = linspace(.5,5,10);
% trim_y = -linspace(0,4.5,10);
% NP1 = 3;
% NP2 = 4;

% run = 20;
% trim_z = linspace(.2,1.4,11);
% trim_x = linspace(.5,5,10);
% trim_y = -linspace(0,4.5,10);
% NP1 = 3;
% NP2 = 4;

% run = 23;
% trim_z = linspace(.2,.9,15);
% trim_x = linspace(1,4,10);
% trim_y = -linspace(0,4,13);
% NP1 = 3;
% NP2 = 5;


% run = 24;
% trim_z = linspace(.15,.9,16);
% trim_x = linspace(0,5,11);
% trim_y = -linspace(0,5,11);
% NP1 = 4;
% NP2 = 4;


% run = 25;
% trim_z = linspace(.3,.7,11);
% trim_x = linspace(0,5,11);
% trim_y = -linspace(0,5,11);
% NP1 = 3;
% NP2 = 4;

% run = 26;
% trim_z = linspace(.3,.7,11);
% trim_x = linspace(0,5,11);
% trim_y = -linspace(0,5,11);
% NP1 = 3;
% NP2 = 4;

reps = 0:length(trim_z)-1;
N1 = zeros(length(trim_y),length(trim_x),length(reps));
N2 = N1;

for ii = 1:length(reps)
    filePath = [basePath expName '/' date(1:4) '/' date(6:7) '/' date(9:10)...
        '/' num2str(run,'%04d') '/' date(1:4) '-' date(6:7) '-' date(9:10)...
        '_' num2str(run,'%04d') '_' expName '_' num2str(reps(ii),'%02d') '.h5'];

    for jj = 1:length(trim_x)
        for kk = 1:length(trim_y)
            im = im2double(h5read(filePath,['/images/horizontal/fluorescence/'...
                'atoms_shimX_' num2str(abs(trim_x(jj)),'%1.3f') '_shimY_' num2str(abs(trim_y(kk)),'%1.3f')]));
            N1(kk,jj,ii) = sum(im(:));
            N2(kk,jj,ii) = max(imgaussfilt(im,[10,10]),[],'all');
        end
    end
    ii/length(reps)
end

colormap(jet)
N1 = N1 - min(N1(:));
N1 = N1/max(N1(:))*255;

N2 = N2 - min(N2(:));
N2 = N2/max(N2(:))*255;

figure(1)
clf
for ii = 1:length(reps)
    subplot(NP1,NP2,ii)
    image(trim_x,trim_y,squeeze(N1(:,:,ii)))
    xlabel('$I_x$ (A)')
    ylabel('$I_y$ (A)')
    axis square
    set(gca,'YDir','normal')
    title(['$I_z = ' num2str(trim_z(ii),'%0.3f') '$ A'])
    colorbar
end
saveas(gcf,['D:\labscript\Experiments\SrMain\quick_trim_sweep\2024\04\03\run_' num2str(run) '_total.png'])

figure(2)
clf
for ii = 1:length(reps)
    subplot(NP1,NP2,ii)
    image(trim_x,trim_y,squeeze(N2(:,:,ii)))
    xlabel('$I_x$ (A)')
    ylabel('$I_y$ (A)')
    axis square
    set(gca,'YDir','normal')
    title(['$I_z = ' num2str(trim_z(ii),'%0.3f') '$ A'])
    colorbar
end
saveas(gcf,['D:\labscript\Experiments\SrMain\quick_trim_sweep\2024\04\03\run_' num2str(run) '_peak.png'])

% figure(3)
% clf
% N3 = N2.*N1;
% N3 = N3./max(N3(:))*255;
% for ii = 1:length(reps)
%     subplot(NP1,NP2,ii)
%     image(trim_x,trim_y,squeeze(N3(:,:,ii)))
%     xlabel('$I_x$ (A)')
%     ylabel('$I_y$ (A)')
%     axis square
%     set(gca,'YDir','normal')
%     title(['$I_z = ' num2str(trim_z(ii),'%0.3f') '$ A'])
%     colorbar
% end