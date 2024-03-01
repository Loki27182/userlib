clear all
% close all
clc

r0 = [0,  eps, -1;...
    0,  0,  1];
u0 = [0,  0, 1;...
    0,  0,  -1];
i0 = [200;...
    200];
a0 = [2;...
    2];

yrange = [-3.748,3.748];
zrange = [-6,6];

n_im_y = 300;
n_vectors_y = 22;

B_max_im = 1;
B_max_q = 1;
dB_scale = 1e-0;

sl_sc = 0.1;
vec_len = .67;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
xrange = 2*yrange/n_im_y;

y = linspace(yrange(1),yrange(2),n_im_y+1);
if exist('xrange','var')
    x = linspace(xrange(1),xrange(2),...
        floor((n_im_y)*diff(xrange)/diff(yrange))+1);
else
    x = y;
end

if exist('zrange','var')
    z = linspace(zrange(1),zrange(2),...
        floor((n_im_y)*diff(zrange)/diff(yrange))+1);
else
    z = y;
end

tic
[B0_1,Bv_1,xm_1,ym_1,zm_1] = fieldSim(x,y,z,r0,u0,i0,a0);
t(1) = toc; 

tic
[B0_2,Bv_2,xm_2,ym_2,zm_2] = stableFieldSim2(x,y,z,r0,u0,i0,a0);
t(2) = toc;

if ~isequal(xm_1,xm_2) || ~isequal(ym_1,ym_2) || ...
        ~isequal(zm_1,zm_2)
    error('Output meshes do not match')
end

B0_1 = B0_1*1e4;
B0_2 = B0_2*1e4;
Bv_1 = Bv_1*1e4;
Bv_2 = Bv_2*1e4;

xmiddle = floor((length(x)+1)/2);
n_skip = floor(n_im_y/(n_vectors_y-1));

yq = squeeze(ym_1(1:n_skip:end,xmiddle,1:n_skip:end))';
zq = squeeze(zm_1(1:n_skip:end,xmiddle,1:n_skip:end))';
ys = squeeze(ym_1(:,xmiddle,:))';
zs = squeeze(zm_1(:,xmiddle,:))';
yim = y;
zim = z;

Bsc_1 = squeeze(B0_1(1:n_skip:end,xmiddle,1:n_skip:end))'/B_max_q;
sc_mask_1 = Bsc_1 > 1;
Bqy_1 = squeeze(Bv_1(1:n_skip:end,xmiddle,1:n_skip:end,2))'; 
Bqz_1 = squeeze(Bv_1(1:n_skip:end,xmiddle,1:n_skip:end,3))'; 
Bqy_1(sc_mask_1) = Bqy_1(sc_mask_1)./Bsc_1(sc_mask_1);
Bqz_1(sc_mask_1) = Bqz_1(sc_mask_1)./Bsc_1(sc_mask_1);
Bqy_1 = Bqy_1/B_max_q*diff(yrange)*vec_len/(n_vectors_y-1);
Bqz_1 = Bqz_1/B_max_q*diff(yrange)*vec_len/(n_vectors_y-1);
Bsy_1 = squeeze(Bv_1(:,xmiddle,:,2))'; 
Bsz_1 = squeeze(Bv_1(:,xmiddle,:,3))'; 
Bim_1 = squeeze(B0_1(:,xmiddle,:))'*255/B_max_im+1;

Bsc_2 = squeeze(B0_2(1:n_skip:end,xmiddle,1:n_skip:end))'/B_max_q;
sc_mask_2 = Bsc_2 > 2;
Bqy_2 = squeeze(Bv_2(1:n_skip:end,xmiddle,1:n_skip:end,2))'; 
Bqz_2 = squeeze(Bv_2(1:n_skip:end,xmiddle,1:n_skip:end,3))'; 
Bqy_2(sc_mask_2) = Bqy_2(sc_mask_2)./Bsc_2(sc_mask_2);
Bqz_2(sc_mask_2) = Bqz_2(sc_mask_2)./Bsc_2(sc_mask_2);
Bqy_2 = Bqy_2/B_max_q*diff(yrange)*vec_len/(n_vectors_y-1);
Bqz_2 = Bqz_2/B_max_q*diff(yrange)*vec_len/(n_vectors_y-1);
Bsy_2 = squeeze(Bv_2(:,xmiddle,:,2))'; 
Bsz_2 = squeeze(Bv_2(:,xmiddle,:,3))'; 
Bim_2 = squeeze(B0_2(:,xmiddle,:))'*255/B_max_im+1;

figure(1)
% clf
subplot(1,3,1)
image(yim,zim,Bim_1)
colormap default
set(gca,'YDir','normal')
set(gca,'TickLabelInterpreter','latex')
cb = colorbar; 
cb.Ticks = linspace(1,256,6); 
cb.TickLabels = ...
    arrayfun(@(nn) num2str(nn,'%0.1f'),...
    linspace(0,B_max_im,6),'UniformOutput',0);
cb.Label.Interpreter = 'latex';
cb.Label.String = '$|B|$ (G)';
cb.Label.FontSize = 14;
cb.TickLabelInterpreter = 'latex'; 
xlabel('$Y$ (m)','Interpreter','latex','FontSize',14)
ylabel('$Z$ (m)','Interpreter','latex','FontSize',14)
grid on
hold on
qv = quiver(yq,zq,Bqy_1,Bqz_1,'AutoScale',0);
qv.Color = [1,.05,.05];
qv.LineWidth = 1;
sl = streamslice(ys,zs,Bsy_1,Bsz_1,sl_sc);
set(sl,'Color',[.85,1,.85])
set(sl,'LineWidth',1);
hold off
title('Standard Implementation',...
    'Interpreter','latex','FontSize',18)
axis equal
axis tight

subplot(1,3,2)
image(yim,zim,Bim_2)
colormap default
set(gca,'YDir','normal')
set(gca,'TickLabelInterpreter','latex')
cb = colorbar; 
cb.Ticks = linspace(1,256,6); 
cb.TickLabels = ...
    arrayfun(@(nn) num2str(nn,'%0.1f'),...
    linspace(0,B_max_im,6),'UniformOutput',0);
cb.Label.Interpreter = 'latex';
cb.Label.String = '$|B|$ (G)';
cb.TickLabelInterpreter = 'latex'; 
cb.Label.FontSize = 14; 
xlabel('$Y$ (m)','Interpreter','latex','FontSize',14)
ylabel('$Z$ (m)','Interpreter','latex')
grid on
hold on
qv = quiver(yq,zq,Bqy_2,Bqz_2,'AutoScale',0);
qv.Color = [1,.05,.05];
qv.LineWidth = 1;
sl = streamslice(ys,zs,Bsy_2,Bsz_2,sl_sc);
set(sl,'Color',[.85,1,.85])
set(sl,'LineWidth',1);
hold off
title('Stable Implementation',...
    'Interpreter','latex','FontSize',18)
axis equal
axis tight

subplot(1,3,3)
image(yim,zim,abs(Bim_1-Bim_2)/dB_scale)
colormap default
set(gca,'YDir','normal')
set(gca,'TickLabelInterpreter','latex')
cb = colorbar; 
cb.Ticks = linspace(1,256,6); 
cb.TickLabels = ...
    arrayfun(@(nn) num2str(nn,'%0.1e'),...
    linspace(0,B_max_im*dB_scale,6),'UniformOutput',0);
cb.Label.Interpreter = 'latex';
cb.Label.String = '$|B|$ (G)';
cb.TickLabelInterpreter = 'latex'; 
cb.Label.FontSize = 14; 
xlabel('$Y$ (m)','Interpreter','latex','FontSize',14)
ylabel('$Z$ (m)','Interpreter','latex')
grid on
hold on
qv = quiver(yq,zq,Bqy_2-Bqy_1,Bqz_2-Bqz_1,'AutoScale',0);
qv.Color = [1,.05,.05];
qv.LineWidth = 1;
hold off
title('Difference',...
    'Interpreter','latex','FontSize',18)
axis equal
axis tight

disp(['Standard Implementation: t = ' num2str(t(1),'%1.2f') ' s'])
disp(['Stable Implementation: t = ' num2str(t(2),'%1.2f') ' s'])
disp(['Stable Implementation is ' num2str(t(2)/t(1),'%1.1f') ...
    ' times slower'])