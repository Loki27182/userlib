clear
clc


tic
save_fig = true;
output_filename = 'frequency_sweep';
datapath = 'D:\misc\2024\06\01\frequency_sweep\';
% files = dir([datapath '*.CSV']);
% t = cellfun(@(x) datetime(x),{files.date});
% [t,idx] = sort(t);
% t = t - days(1) + hours(14) - minutes(16) - seconds(8);
% files = files(idx);
% n = cellfun(@(x) str2double(x(1:end-4)),{files.name});
n = 0:44;
f = 325.1548:.0001:325.1592;
files = arrayfun(@(x) [datapath 'ALL' num2str(x,'%04d') '\F' num2str(x,'%04d') 'CH1.CSV'],n,'UniformOutput',false);

shot_data = cellfun(@(x) analyze_shot(x),files);
% shot_data = shot_data(1:1400);

sig = [shot_data.sig];
sig_plot = [shot_data.sig_plot];
peak_height = max(sig_plot,[],1)';

l_cav = shot_data.l_cav;
l_plot = mean([shot_data.l_cav_plot],2);
l_edge = [shot_data.l_edge];

FWHM_edges = [shot_data.FWHM_l]';
left_edges_n = FWHM_edges(:,1)';
right_edges_n = FWHM_edges(:,2)';

FWHM = [shot_data.FWHM]';


if save_fig
    fid = gcf;
    fid.Units = 'inches';
    fid.InnerPosition(3:4) = [11,8.5];
    fid.PaperSize = fid.InnerPosition(3:4);
    print([datapath output_filename '.pdf'],'-dpdf')
    print([datapath output_filename '.emf'],'-dmeta')
    savefig([datapath output_filename '.fig'])
end

clf
subplot(2,2,1)
imagesc(f,l_cav,sig)
xlabel('Laser frequency (THz)','FontSize',14)
ylabel('$V_\mathrm{PZT}$ (arb)','FontSize',14)

subplot(2,2,2)
plot(f,-left_edges_n,f,-right_edges_n)
xlabel('Laser frequency (THz)','FontSize',14)
ylabel('$V_\mathrm{PZT}$ (arb)','FontSize',14)

subplot(2,2,3)
plot(f,FWHM)
xlabel('Laser frequency (THz)','FontSize',14)
ylabel('FWHM (arb)','FontSize',14)
ylim([0,.28])

subplot(2,2,4)
plot(f,peak_height)
xlabel('Laser frequency (THz)','FontSize',14)
ylabel({'Peak intracavity','power (arb)'},'FontSize',14)
ylim([0,.97])

function shot_data = analyze_shot(filepath,varargin)
if nargin==2
    n_sm = varargin{1};
else
    n_sm = 10;
end
% filepath = [fileInfo.folder ,'\' fileInfo.name];
shot_data.all = readmatrix(filepath,'Range',[19,4]);
shot_data.l_cav = (shot_data.all(1:2475,1) - shot_data.all(1,1))*338;
shot_data.sig = smooth(shot_data.all(1:2475,2),n_sm)*25;
shot_data.l_cav = shot_data.l_cav(20:end-20);
shot_data.sig = shot_data.sig(20:end-20);
shot_data = rmfield(shot_data,'all');
shot_data.sig_slope = abs(diff(shot_data.sig)/max(abs(diff(shot_data.sig))));
shot_data.idx_edge = find(shot_data.sig_slope==max(shot_data.sig_slope),1);
shot_data.l_edge = shot_data.l_cav(shot_data.idx_edge);

mask = 0*shot_data.l_cav==0;%shot_data.l_cav < shot_data.l_edge + .25 & ...
    %shot_data.l_cav > shot_data.l_edge - .75;

shot_data.is_bad = ~( mask(1) || mask(end) );
if ~shot_data.is_bad
    shot_data.sig_plot = shot_data.sig(mask);
    shot_data.l_cav_plot = shot_data.l_cav(mask) - shot_data.l_edge;
    shot_data.sig_plot = shot_data.sig_plot - ...
        polyfit(1:101,shot_data.sig_plot([1:50,end-50:end]),0);

    shot_data.FWHM_l = shot_data.l_cav_plot([find(shot_data.sig_plot>=max(shot_data.sig_plot)/2,1,'first'),...
        find(shot_data.sig_plot>=max(shot_data.sig_plot)/2,1,'last')]);
    shot_data.FWHM_sig = max(shot_data.sig_plot)/2*[1,1];
    shot_data.FWHM = abs(diff(shot_data.FWHM_l));
else
    shot_data.sig_plot = [];
    shot_data.l_cav_plot = [];
    shot_data.FWHM_l = [];
    shot_data.FWHM_sig = [];
    shot_data.FWHM = [];
end
end