clear
clc

rng(1)

n_atoms = 1e3;
n_plot = 1e3;
n_skip = floor(n_atoms/n_plot);

dt = 1e-6;
t_f = 100e-3;
T = 690e-9;
w_cloud = [500e-6,500e-6,150e-6];
n_t_skip = 10;

dx_mesh = 1e-5;
l_mesh = w_cloud.*[.5,4,2];

l_plot_x = l_mesh(1);
l_plot_y = l_mesh(2);
l_plot_z = l_mesh(3);

P = 4;
w0 = 70e-6;
lam_dipole = 813e-9;
lam_trans = 460.861983e-9;
m = 87.9/6.022e26;

kB = 1.38e-23;
h = 6.626e-34;
hbar = h/(2*pi);
c = 299792458;

f_dipole = c/lam_dipole;
f_trans = c/lam_trans;
Delta = 2*pi*(f_dipole - f_trans);
Gamma = 2*pi*30e6;

x = -l_mesh(1):dx_mesh:l_mesh(1);
y = -l_mesh(2):dx_mesh:l_mesh(2);
z = -l_mesh(3):dx_mesh:l_mesh(3);
[x_m,y_m,z_m] = meshgrid(x,y,z);

U_m = reshape(U([x_m(:)';y_m(:)';z_m(:)'],...
    P,w0,lam_dipole,Gamma,Delta,f_trans),size(x_m));
x_grad = x(2:end-1);
y_grad = y(2:end-1);
z_grad = z(2:end-1);
[x_grad_m,y_grad_m,z_grad_m] = meshgrid(x_grad,y_grad,z_grad);

a_x = -(diff(U_m(:,2:end,:),1,2) + diff(U_m(:,1:end-1,:),1,2))/...
    (2*m*dx_mesh);
a_y = -(diff(U_m(2:end,:,:),1,1) + diff(U_m(1:end-1,:,:),1,1))/...
    (2*m*dx_mesh);
a_z = -(diff(U_m(:,:,2:end),1,3) + diff(U_m(:,:,1:end-1),1,3))/...
    (2*m*dx_mesh)-9.8;

a_x = a_x(2:end-1,:,2:end-1);
a_y = a_y(:,2:end-1,2:end-1);
a_z = a_z(2:end-1,2:end-1,:);

r = randn(3,n_atoms).*repmat(w_cloud',1,n_atoms);
v = randn(3,n_atoms)*sqrt(kB*T/m);
a = zeros(size(r));

figure(1)
clf
subplot(1,2,1)
p1 = plot3(r(1,1:n_skip:end),r(2,1:n_skip:end),r(3,1:n_skip:end),'.b');
axis equal
xlim([-l_plot_x,l_plot_x]*1e3)
ylim([-l_plot_y,l_plot_y]*1e3)
zlim([-l_plot_z,l_plot_z]*1e3)
xlabel('x (mm)')
ylabel('y (mm)')
zlabel('z (mm)')
% hold on
% p2 = plot3(r(1,1:n_skip:end),...
%     r(2,1:n_skip:end),...
%     -l_plot_z*1e3*ones(size(r(1,1:n_skip:end))),...
%     '.b');
% p3 = plot3(r(1,1:n_skip:end),...
%     l_plot_y*1e3*ones(size(r(1,1:n_skip:end))),...
%     r(3,1:n_skip:end),...
%     '.b');
% p4 = plot3(l_plot_x*1e3*ones(size(r(1,1:n_skip:end))),...
%     r(2,1:n_skip:end),...
%     r(3,1:n_skip:end),...
%     '.b');
% hold off

N = 100;
subplot(1,2,2)
p5 = plot(0,N);
ylim([0,100])

t = 0:dt:t_f;

x_grad_m = gpuArray(x_grad_m);
y_grad_m = gpuArray(y_grad_m);
z_grad_m = gpuArray(z_grad_m);
a_x = gpuArray(a_x);
a_y = gpuArray(a_y);
a_z = gpuArray(a_z);
r = gpuArray(r);
v = gpuArray(v);
a = gpuArray(a);
a_x_ii = gpuArray(zeros(size(r)));
a_y_ii = gpuArray(zeros(size(r)));
a_z_ii = gpuArray(zeros(size(r)));

for ii = 1:length(t)
    a_x_ii = interp3(x_grad_m,y_grad_m,z_grad_m,a_x,r(1,:),r(2,:),r(3,:));
    a_y_ii = interp3(x_grad_m,y_grad_m,z_grad_m,a_y,r(1,:),r(2,:),r(3,:));
    a_z_ii = interp3(x_grad_m,y_grad_m,z_grad_m,a_z,r(1,:),r(2,:),r(3,:));
    a = [a_x_ii;a_y_ii;a_z_ii];
    v = v + dt*a;
    r = r + v*dt;
    if mod(ii,n_t_skip)==0
        ri = gather(r);
        p1.XData = ri(1,1:n_skip:end)*1e3;
        p1.YData = ri(2,1:n_skip:end)*1e3;
        p1.ZData = ri(3,1:n_skip:end)*1e3;

        % p2.XData = p1.XData;
        % p2.YData = p1.YData;
        % 
        % p3.XData = p1.XData;
        % p3.ZData = p1.ZData;
        % 
        % p4.YData = p1.YData;
        % p4.ZData = p1.ZData;

        
        subplot(1,2,1)
        title(['$t = ' num2str(t(ii)*1e3,'%1.1f') '$ ms -- $N = ' ...
            num2str(sum(~isnan(p1.YData))/n_plot*100,'%1.2f') '$'],...
            'FontSize',16)
        
        p5.XData = [p5.XData, (t + dt)*1e3];
        p5.YData = [p5.YData, sum(~isnan(p1.YData))/n_plot*100];

        drawnow
        
        disp(num2str(ii/length(t)*100,'%1.2f'))
    end
end

function U = U(r,P,w0,lam,Gamma,Delta,f_trans)
omega_0 = 2*pi*f_trans;
c = 299792458;
U = 3*pi*c^2*Gamma/(2*omega_0^3*Delta)*I(r,P,w0,lam).*...
    (cos(2*pi*r(2,:)/(lam/2))+1);
end

function I = I(r,P,w0,lam)
zR = pi*w0^2/lam;
w = w0*sqrt(1+(r(2,:)/zR).^2);
I0 = 2*P./(pi*w.^2);
I = I0.*exp(-2*(r(1,:).^2+r(3,:).^2)./w.^2);
end