
% name = 'Both repumps on';
% parameter = 'BlueMOTLoadTime';
% run = 21;
% reps = 0:120;

% name = '679 repump only';
% parameter = 'BlueMOTLoadTime';
% run = 22;
% reps = 0:120;

name = '707 repump only';
parameter = 'BlueMOTLoadTime';
run = 22;
reps = 0:80;
% 
% name = 'No repump';
% parameter = 'BlueMOTLoadTime';
% run = 22;
% reps = 0:120;

basepath = 'D:\labscript\Experiments\SrMain\red_MOT_VCO_ramp\2024\04\26\';
x = loadParameters('red_MOT_VCO_ramp','2024/04/26',run,reps,parameter);
n = loadParameters('red_MOT_VCO_ramp','2024/04/26',run,reps,'absorption/atomNumber','/results/single_shot_analysis/');
[x,idx] = sort(x);
n = n(idx);

plot(x,n/1e6)
xlabel('Load time (s)','FontSize',14)
ylabel('Atom number ($\times 10^6$)','FontSize',14)
title(name,'FontSize',16)
saveas(gcf,[basepath num2str(run,'%04d') '\results.png'])
savefig([basepath num2str(run,'%04d') '\results.fig'])