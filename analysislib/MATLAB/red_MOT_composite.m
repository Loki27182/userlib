clear
clc

f=loadParameters('new_red_MOT_test','2024/01/04',44,0:49,{'RedCoolingBeatnote'});
n=loadParameters('new_red_MOT_test','2024/01/04',44,0:49,{'atomNumber'},'/results/single_gaussian_analysis');
[a,b] = loadFluorescence('new_red_MOT_test','2024/01/04',44,0:49);

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

saveas(gcf,'composite_global_scaling.png')

figure(2)
for ii = 1:length(idx)
    subplot(5,10,ii)
    imagesc(d(:,:,ii))
    axis image
    axis off
end

saveas(gcf,'composite_individual_scaling.png')