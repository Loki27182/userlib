clear
clc

runs = 10:20;
fr = cell(1,length(runs));
t0 = zeros(1,length(runs));
df0 = [7,6.3,6,5,6];

figure(1)
clf
for ii = 1:length(runs)
reps = 0:80;

f = loadParameters('red_light_magnetometry','2024/04/15',runs(ii),reps,'RedBeatnote');
N = loadParameters('red_light_magnetometry','2024/04/15',runs(ii),reps,'atomNumber','/results/single_gaussian_analysis/');
t0(ii) = loadParameters('red_light_magnetometry','2024/04/15',runs(ii),0,'TimeOfFlight');
[xData, yData] = prepareCurveData( f, N );

a0 = max(yData)-min(yData);

% Set up fittype and options.
ft = fittype( '-a*exp(-(x-d)^2/e^2)-b*exp(-(x-d-f)^2/e^2)-c*exp(-(x-d+f)^2/e^2)+g+h*x', 'independent', 'x', 'dependent', 'y' );
opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
opts.Display = 'Off';
opts.StartPoint = [a0 a0 a0 1155 2 6 max(yData) 0];

fr{ii} = fit( xData, yData, ft, opts );

subplot(3,4,ii)
plot(xData,yData,'x',xData,fr{ii}(xData),'--')
xlabel('Beatnote frequency (MHz)','FontSize',12)
ylabel('Atom number (arb)','FontSize',12)
title(['Run ' num2str(runs(ii))],'FontSize',14)
end

savefig('D:\labscript\Experiments\SrMain\red_light_magnetometry\2024\04\15\field_decay_fits.fig')
saveas(gcf,'D:\labscript\Experiments\SrMain\red_light_magnetometry\2024\04\15\field_decay_fits.png')

df = cellfun(@(x) x.f,fr);
ddf = cellfun(@(x) getddf(x),fr);
[xData,idx] = sort(t0*1e3);
yData = df(idx);

[xData, yData] = prepareCurveData( xData,yData );
ft = fittype( 'a*exp(-x/b)+c', 'independent', 'x', 'dependent', 'y' );
opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
opts.Display = 'Off';
opts.StartPoint = [2,.2,5.5];

exp_fit = fit( xData, yData, ft, opts );
xf = linspace(0,max(xData),100);
yf = exp_fit(xf);

figure(2)
errorbar(xData,yData,ddf,'x')
hold on
plot(xf,yf,'--')
hold off
ylim([4,8])
xlabel('Time of flight (ms)','FontSize',14)
ylabel('Peak separation (MHz)','FontSize',14)
legend('Data',['Fit: $\tau = ' num2str(exp_fit.b,'%1.2f') '$ ms'])

savefig('D:\labscript\Experiments\SrMain\red_light_magnetometry\2024\04\15\field_decay.fig')
saveas(gcf,'D:\labscript\Experiments\SrMain\red_light_magnetometry\2024\04\15\field_decay.png')

function ddf = getddf(fr)
ci = confint(fr);
ddf = diff(ci(:,6))/4;
end

