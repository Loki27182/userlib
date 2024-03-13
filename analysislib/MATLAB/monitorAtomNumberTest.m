clc
clear
n = 1000;

%set(gcf, 'KeyPressFcn', @KeyPressedFcn)
path = ['D:/labscript/Experiments/SrMain/basic_blue_MOT/2024/03/06/0006/'...
    '2024-03-06_0006_basic_blue_MOT_0'];
N = zeros(1,n);
t = zeros(1,n);
dt = 3.16;
for ii = 1:n
    fileName = [path '_rep' num2str(ii,'%05d') '.h5' ];
    N(ii) = h5readatt(fileName,'/results/continuous_fluorescence_single','atomNumber');

    %rep_str = num2str(runs(ii),['%0' num2str(n_digits) 'd']);
    strs = split(h5readatt(fileName,'/','run time'),'T');
    t(ii) = str2double(strs{2}(1:2))*3600 + str2double(strs{2}(3:4))*60 + str2double(strs{2}(5:end));

end

N_plot = N/mean(N);
N_mean = mean(N_plot)*ones(1,ii);
dN = std(N_plot)*ones(1,ii);
t_plot = t/3600;


subplot(1,3,1)
plot(t_plot,N_plot,'x',t_plot,N_mean,'--k',...
    t_plot,N_mean-dN,':k',...
    t_plot,N_mean+dN,':k')
ylim([0,1.1])
xlabel('Time (hr)')
ylabel({'Atom Number','(Normalized to mean)'})

subplot(1,3,2)
histogram(N_plot,30)
xlabel({'Atom Number','(Normalized to mean)'})
ylabel('Counts')

[avar,tau] = allanvar(N_plot,unique(floor(logspace(0,log10(n/2-1),200))),1/mean(diff(t_plot)));

subplot(1,3,3)
semilogx(tau,sqrt(avar)*100)
xlabel('$\tau$ (hr)')
ylabel('$\sigma_N(\tau)$ (\%)')

savefig('D:\labscript\Experiments\SrMain\basic_blue_MOT\2024\03\06\0006\plots.fig')
saveas(gcf,'D:\labscript\Experiments\SrMain\basic_blue_MOT\2024\03\06\0006\plots.jpg')
