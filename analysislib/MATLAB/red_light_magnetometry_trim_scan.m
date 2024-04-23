clc
clear

% [s,ds,i]=getSep(64,'BlueMOTShimY')

% param = 'BlueMOTShimZ';
% runs = 21:36;
% r_invert = 32;
% 
% param = 'BlueMOTShimX';
% runs = [23,38:48];
% r_invert = 44;
% % 
param = 'BlueMOTShimY';
runs = 50:64;
r_invert = 61;

if exist('runs','var')>0
s = zeros(size(runs));
ds = s;
i_trim = s;

for ii = 1:length(runs)
    [s_i,ds_i,i_trim_i] = getSep(runs(ii),param);
    s(ii) = s_i;
    ds(ii) = ds_i;
    i_trim(ii) = i_trim_i;
end

i_trim(runs>=r_invert) = -i_trim(runs>=r_invert);

[xData, yData] = prepareCurveData( i_trim, s );
ft = fittype( 'sqrt(a^2+(x-b)^2/c^2)', 'independent', 'x', 'dependent', 'y' );
opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
opts.Display = 'Off';
opts.StartPoint = [3.5, .1, .5];

fr = fit( xData, yData, ft, opts );
i_f = linspace(min(i_trim),max(i_trim),100);
s_f = fr(i_f);

errorbar(i_trim,s,ds,'x')
hold on
plot(i_f,s_f,'--')
hold off
ylim([0,6])
xlabel(param,'FontSize',14)
ylabel('Peak separation (MHz)','FontSize',14)
legend('Data',['Fit: $I_0 = ' num2str(fr.b,'%1.3f') '$ A'],'Location','north')

savefig(['D:\labscript\Experiments\SrMain\red_light_magnetometry\2024\04\15\' param '_scan.fig'])
saveas(gcf,['D:\labscript\Experiments\SrMain\red_light_magnetometry\2024\04\15\' param '_scan.png'])
end
function [sep,dsep,i_trim] = getSep(run,param)
reps = 0:80;

f = loadParameters('red_light_magnetometry','2024/04/15',run,reps,'RedBeatnote');
N = loadParameters('red_light_magnetometry','2024/04/15',run,reps,'atomNumber','/results/single_gaussian_analysis/');
i_trim = loadParameters('red_light_magnetometry','2024/04/15',run,0,param);
f(N<0|N>1e8) = [];
N(N<0|N>1e8) = [];

[xData, yData] = prepareCurveData( f, N );

a0 = max(yData)-min(yData);

% Set up fittype and options.
ft = fittype( '-a*exp(-(x-d)^2/e^2)-b*exp(-(x-d-f)^2/e^2)-c*exp(-(x-d+f)^2/e^2)+g+h*x', 'independent', 'x', 'dependent', 'y' );
opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
opts.Display = 'Off';
opts.StartPoint = [a0 a0 a0 1155 2 4.5 max(yData) 0];

fr = fit( xData, yData, ft, opts );
sep = fr.f;
dsep = diff(confint(fr))/4;
dsep = dsep(6);
end