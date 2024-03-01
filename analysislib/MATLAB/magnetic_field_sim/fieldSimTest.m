clear
clc

i_sol = .05;
i_grad = .02;

ymax = 0.08;
dx = 2.5e-4;
z_scale = 1.75;

maxB = 450;

nQuiver = 31;
edgeCutoff = 10;
rMask = .004;

z0 = readmatrix('loop_heights.csv')/1e3;
n_loops = length(z0);

r0 = [zeros(n_loops,2),z0];
r0 = [r0;0,0,.004;0,0,.076];

u0 = [repmat([0,0,1],n_loops,1);0,0,-1;0,0,1];
i0 = [repmat(i_sol,n_loops,1);repmat(9*i_grad,2,1)];
a0 = [repmat(.0245,n_loops,1);repmat(.032,2,1)];

y = -ymax:dx:ymax;
x = -5*dx:dx:5*dx;
z = ((z_scale+1)*min(z0)-max(z0))/z_scale:dx:((z_scale+1)*max(z0)-min(z0))/z_scale;

nElements = length(x)*length(y)*length(z)*61;
disp(['Number of elements is approximately ' num2str(nElements,'%0.1e')])
if nElements > 4e8
    error('Mesh is too large')
end

[B,B_v,x_m,y_m,z_m]=...
    fieldSim(x,y,z,r0,u0,i0,a0);

B_v = B_v*1e7;
B = B*1e7;
x_m = x_m*1e2;
y_m = y_m*1e2;
z_m = z_m*1e2;
x = x*1e2;
y = y*1e2;
z = z*1e2;

nSkip = floor(length(y)/nQuiver);

xmiddle = floor((length(x)+1)/2);
ymiddle = floor((length(y)+1)/2);
Byz = squeeze(B_v(edgeCutoff+1:nSkip:end-edgeCutoff,xmiddle,edgeCutoff+1:nSkip:end-edgeCutoff,2:3));
Bmag = squeeze(B(edgeCutoff+1:end-edgeCutoff,xmiddle,edgeCutoff+1:end-edgeCutoff))';
yyz = squeeze(y_m(edgeCutoff+1:nSkip:end-edgeCutoff,xmiddle,edgeCutoff+1:nSkip:end-edgeCutoff));
zyz = squeeze(z_m(edgeCutoff+1:nSkip:end-edgeCutoff,xmiddle,edgeCutoff+1:nSkip:end-edgeCutoff));

Byz = reshape(Byz,numel(Byz)/2,2);
yyz = reshape(yyz,numel(yyz),1); 
zyz = reshape(zyz,numel(zyz),1); 

divB = divergence(x_m,y_m,z_m,...
    squeeze(B_v(:,:,:,1)),squeeze(B_v(:,:,:,2)),squeeze(B_v(:,:,:,3)));
[curlBx,curlBy,curlBz] = curl(x_m,y_m,z_m,...
    squeeze(B_v(:,:,:,1)),squeeze(B_v(:,:,:,2)),squeeze(B_v(:,:,:,3)));
curlB = sqrt(curlBx.^2+curlBy.^2+curlBz.^2);
[BgradX,BgradY,BgradZ] = gradient(B,mean(diff(x)),mean(diff(y)),mean(diff(y)));
Bgrad = sqrt(BgradX.^2+BgradY.^2+BgradZ.^2);


Byz_n = sqrt(sum(Byz.^2,2));
Byz(Byz_n>maxB) = ...
    Byz(Byz_n>maxB)*maxB./Byz_n(Byz_n>maxB);

y1 = y(edgeCutoff+1:end-edgeCutoff);
z1 = z(edgeCutoff+1:end-edgeCutoff);
[y1_m,z1_m] = meshgrid(y1,z1);

gradPlot = squeeze(Bgrad(edgeCutoff+1:end-edgeCutoff,xmiddle,edgeCutoff+1:end-edgeCutoff))';
divPlot = abs(squeeze(divB(edgeCutoff+1:end-edgeCutoff,xmiddle,edgeCutoff+1:end-edgeCutoff)))';
divRatio = divPlot./gradPlot;
curlPlot = abs(squeeze(curlB(edgeCutoff+1:end-edgeCutoff,xmiddle,edgeCutoff+1:end-edgeCutoff)))';
curlRatio = curlPlot./gradPlot;

rMask = rMask*1e2;
for ii = 1:size(r0,1)
    mask = ((a0(ii)*1e2 - y1_m).^2 + (r0(ii,3)*1e2 - z1_m).^2) < rMask^2 | ...
        ((-a0(ii)*1e2 - y1_m).^2 + (r0(ii,3)*1e2 - z1_m).^2) < rMask^2;
    gradPlot(mask) = 0;
    divPlot(mask) = 0;
    divRatio(mask) = 0;
    curlPlot(mask) = 0;
    curlRatio(mask) = 0;
end

clf
subplot(2,4,1)
q = quiver(yyz,zyz,Byz(:,1),Byz(:,2));
% q.ShowArrowHead = false;
axis equal
grid on
title({'Magnetic Field','Vectors'})

subplot(2,4,5)
imagesc(y1,z1,Bmag)
colorbar
set(gca,'YDir','normal')
grid on
axis equal
clim([0,maxB])
title({'Magnetic Field','Magnitude'})

subplot(2,4,2)
imagesc(y1,z1,gradPlot)
colorbar
set(gca,'YDir','normal')
grid on
axis equal
title({'Magnitude of Magnetic','Field Gradient'})
% clim([0,1e1])

subplot(2,4,3)
imagesc(y1,z1,divPlot)
colorbar
set(gca,'YDir','normal')
grid on
axis equal
title({'Magnitude of Magnetic','Field Divergence'})
% clim([0,1e1])

subplot(2,4,4)
imagesc(y1,z1,divRatio)
colorbar
set(gca,'YDir','normal')
grid on
axis equal
title({'Divergence/Gradient','Ratio'})
% clim([0,1e0])

subplot(2,4,6)
imagesc(y1,z1,gradPlot)
colorbar
set(gca,'YDir','normal')
grid on
axis equal
title({'Magnitude of Magnetic','Field Gradient'})
% clim([0,1e1])

subplot(2,4,7)
imagesc(y1,z1,curlPlot)
colorbar
set(gca,'YDir','normal')
grid on
axis equal
title({'Magnitude of Magnetic','Field Curl'})
% clim([0,1e1])

subplot(2,4,8)
imagesc(y1,z1,curlRatio)
colorbar
set(gca,'YDir','normal')
grid on
axis equal
title({'Curl/Gradient','Ratio'})

% savefig('t_cubed_field')