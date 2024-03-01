close all
clear all
clc

i_sol = .05;
i_grad = .02;

ymax = 0.08;
dx = 2e-3;
z_scale = 1.75;

z0 = readmatrix('loop_heights.csv')/1e3;
n_loops = length(z0);

r0 = [zeros(n_loops,2),z0];
r0 = [r0;0,0,.004;0,0,.076];

u0 = [repmat([0,0,1],n_loops,1);0,0,-1;0,0,1];
i0 = [repmat(i_sol,n_loops,1);repmat(9*i_grad,2,1)];
a0 = [repmat(.0245,n_loops,1);repmat(.032,2,1)];

y = -ymax:dx:ymax;
x = -ymax:dx:ymax;
z = ((z_scale+1)*min(z0)-max(z0))/z_scale:dx:((z_scale+1)*max(z0)-min(z0))/z_scale;

nElements = length(x)*length(y)*length(z)*(n_loops+2);
disp(['Number of elements is approximately ' num2str(nElements,'%0.1e')])
if nElements > 4e8
    error('Mesh is too large')
end

[B,B_v,x_m,y_m,z_m]=...
    stableFieldSim2(x,y,z,r0,u0,i0,a0);
