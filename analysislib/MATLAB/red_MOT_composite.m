clear
clc

% date = '2024/01/04';
% run = 44;
% reps = 0:49;

% date = '2024/01/05';
% run = 1;
% reps = 0:49;

% run = 2;
% reps = 0:99;

date = '2024/01/08';
run = 5;
reps = 0:49;


expName = 'new_red_MOT_test';

basePath = 'D:/labscript/Experiments/SrMain/';

dataPath = [basePath expName '/' date(1:4) '/' date(6:7) '/' date(9:10)...
    '/' num2str(run,'%04d') '/'];

f=loadParameters(expName,date,run,reps,{'RedCoolingBeatnote'});
n=loadParameters(expName,date,run,reps,{'atomNumber'},'/results/single_gaussian_analysis');
[a,b] = loadFluorescence(expName,date,run,reps);

n_sm = 10;

[f,idx] = sort(f);
n = n(idx);

d = zeros(size(a,2),size(a,1),size(a,3));
for ii = 1:length(idx)
    d(:,:,ii) = imgaussfilt(a(:,:,idx(ii))'-b(:,:,idx(ii))',[n_sm,n_sm]);
end
d = d(1:n_sm/2:end,1:n_sm/2:end,:);
d = d/max(d,[],'all')*255;

figure(1)
for ii = 1:length(idx)
    subplot(5,10,ii)
    image(d(:,:,ii))
    axis image
    axis off
end

saveas(gcf,[dataPath 'composite_global_scaling.png'])

figure(2)
for ii = 1:length(idx)
    subplot(5,10,ii)
    imagesc(d(:,:,ii))
    axis image
    axis off
end

saveas(gcf,[dataPath 'composite_individual_scaling.png'])