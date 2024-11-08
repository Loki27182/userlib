clear
clc

tic
save_fig = true;
output_filename = 'overnight_broadening_monitor';
datapath = 'D:\misc\2024\05\31\overnight_log\LOG\';
n_sm_edges = 30;
files = dir([datapath '*.CSV']);
t = cellfun(@(x) datetime(x),{files.date});
[t,idx] = sort(t);
t = t - days(1) + hours(14) - minutes(16) - seconds(8);
files = files(idx);
n = cellfun(@(x) str2double(x(1:end-4)),{files.name});

shot_data = arrayfun(@(x) analyze_shot(x),files);
shot_data = shot_data(1:1400);
good_mask = ~[shot_data.is_bad];
shot_data = shot_data(good_mask);

t_plot = hours(t - t(1));
t_plot = t_plot(good_mask);
n_shot = 1:sum(good_mask);

sig = [shot_data.sig];
sig_plot = [shot_data.sig_plot];
peak_height = smooth(max(sig_plot,[],1),n_sm_edges)';

l_cav = shot_data.l_cav;
l_plot = mean([shot_data.l_cav_plot],2);
l_edge = smooth([shot_data.l_edge],n_sm_edges);

FWHM_edges = [shot_data.FWHM_l]';
left_edges_n = smooth(FWHM_edges(:,1),n_sm_edges)';
right_edges_n = smooth(FWHM_edges(:,2),n_sm_edges)';

FWHM = smooth([shot_data.FWHM],n_sm_edges)';

dt = diff(t_plot);

jumps = find(abs(dt-mean(dt))>std(dt)*10);

left_edges = left_edges_n;
right_edges = right_edges_n;
for ii = length(jumps):-1:1
    t_plot = [t_plot(1:jumps(ii)),NaN,t_plot(jumps(ii)+1:end)];
    left_edges = [left_edges(1:jumps(ii)),NaN,left_edges(jumps(ii)+1:end)];
    right_edges = [right_edges(1:jumps(ii)),NaN,right_edges(jumps(ii)+1:end)];
    FWHM = [FWHM(1:jumps(ii)),NaN,FWHM(jumps(ii)+1:end)];
    peak_height = [peak_height(1:jumps(ii)),NaN,peak_height(jumps(ii)+1:end)];
end

figure(1)
clf
subplot(2,2,1)
imagesc(1:size(sig,2),l_cav-mean(l_cav),sig)
xlabel('Shot number','FontSize',14)
ylabel('$V_\mathrm{PZT}$ (arb)','FontSize',14)

subplot(2,2,2)
imagesc(n_shot,l_plot,sig_plot)
hold on
plot(n_shot,left_edges_n,'-b',n_shot,right_edges_n,'-r','LineWidth',2)
hold off
xlabel('Shot number','FontSize',14)
ylabel({'$V_\mathrm{PZT}$ (arb)','centered'},'FontSize',14)
% set(gca,'YDir','normal')
cb = colorbar;
ylabel(cb,{'Intracavity power','(arb)'},'Interpreter','latex','FontSize',14)
legend('Broad edge half-max','Sharp edge half-max','Location','northwest','FontSize',8)

subplot(2,3,4)
plot(t_plot,-left_edges,'-b',t_plot,right_edges,'-r','LineWidth',2)
ylabel({'$V_\mathrm{edge}$ (arb)','centered'},'FontSize',14)
xlabel('Time (hours)','FontSize',14)
set(gca,'YDir','normal')
xlim([min(t_plot),max(t_plot)])
ylim([-.075,0.42])
yticks(0:.1:.4)
yticklabels({'0','$-0.1$','$-0.2$','$-0.3$','$-0.4$'})
legend('Broad edge half-max','Sharp edge half-max','Location','east','FontSize',8)

subplot(2,3,5)
plot(t_plot,FWHM,'LineWidth',2)
ylabel('FWHM (arb)','FontSize',14)
xlabel('Time (hours)','FontSize',14)
set(gca,'YDir','normal')
xlim([min(t_plot),max(t_plot)])
ylim([0,.42])
yticks(0:.1:.4)

subplot(2,3,6)
plot(t_plot,peak_height,'LineWidth',2)
ylabel({'Peak intracavity','power (arb)'},'FontSize',14)
xlabel('Time (hours)','FontSize',14)
set(gca,'YDir','normal')
xlim([min(t_plot),max(t_plot)])
ylim([0,1.05])

if save_fig
    fid = gcf;
    fid.Units = 'inches';
    fid.InnerPosition(3:4) = [11,8.5];
    fid.PaperSize = fid.InnerPosition(3:4);
    print([datapath output_filename '.pdf'],'-dpdf')
    print([datapath output_filename '.emf'],'-dmeta')
    savefig([datapath output_filename '.fig'])
end

['Time elapsed: ' num2str(toc,'%1.3f') ' s']

function shot_data = analyze_shot(fileInfo,varargin)
if nargin==2
    n_sm = varargin{1};
else
    n_sm = 10;
end
filepath = [fileInfo.folder ,'\' fileInfo.name];
shot_data.all = readmatrix(filepath,'Range',[19,4]);
shot_data.l_cav = (shot_data.all(1:2475,1) - shot_data.all(1,1))*338;
shot_data.sig = smooth(shot_data.all(1:2475,2),n_sm)*25;
shot_data.l_cav = shot_data.l_cav(20:end-20);
shot_data.sig = shot_data.sig(20:end-20);
shot_data = rmfield(shot_data,'all');
shot_data.sig_slope = abs(diff(shot_data.sig)/max(abs(diff(shot_data.sig))));
shot_data.idx_edge = find(shot_data.sig_slope==max(shot_data.sig_slope),1);
shot_data.l_edge = shot_data.l_cav(shot_data.idx_edge);

mask = shot_data.l_cav < shot_data.l_edge + .25 & ...
    shot_data.l_cav > shot_data.l_edge - .75;

shot_data.is_bad =  mask(1) || mask(end);
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