function [B,B_v,x,y,z] = fieldSim(x_sample,y_sample,z_sample,...
        r0_coils,u0_coils,i0_coils,a0_coils,method)
    arguments
        x_sample (:,1) double {mustBeReal,mustBeFinite,mustBeNonempty}
        y_sample (:,1) double {mustBeReal,mustBeFinite,mustBeNonempty}
        z_sample (:,1) double {mustBeReal,mustBeFinite,mustBeNonempty}
        r0_coils (:,3) double {mustBeReal,mustBeFinite,mustBeNonempty}
        u0_coils (:,3) double {mustBeReal,mustBeFinite,mustBeNonempty}
        i0_coils (:,1) double {mustBeReal,mustBeFinite,mustBeNonempty}
        a0_coils (:,1) double {mustBeReal,mustBeFinite,mustBeNonempty,...
            mustBePositive}
        method string {mustBeMember(method,{'list','meshgrid'})} = ...
            'meshgrid'
    end
    
    if size(u0_coils,1) ~= size(r0_coils,1) ||...
            size(i0_coils,1) ~= size(r0_coils,1) ||...
            size(a0_coils,1) ~= size(r0_coils,1)
        error('All coil parameter lists must have the same number of rows')
    end
    
    switch method
        case 'list'
            if length(x_sample)==length(y_sample) && length(x_sample)==length(y_sample)
                x_s = x_sample;
                y_s = y_sample;
                z_s = z_sample;
            else
                error('For list method, all sample lists must be the same length')
            end
        case 'meshgrid'
            [x_s,y_s,z_s] = meshgrid(x_sample,y_sample,z_sample);
            meshsize = size(x_s);
            x_s = x_s(:);
            y_s = y_s(:);
            z_s = z_s(:);
    end
    
    % mu0 = 1.25663706212e-6;
    % 
    % 
    % x0 = r0_coils(:,1);
    % y0 = r0_coils(:,2);
    % z0 = r0_coils(:,3);
    % 
    % u0x = u0_coils(:,1);
    % u0y = u0_coils(:,2);
    % u0z = u0_coils(:,3);
    % 
    % n_samples = length(x_s);
    % n_coils = length(x0);
    % 
    % [idxn,idxs] = meshgrid(1:n_coils,1:n_samples);
    % 
    % r(:,3,:) = z_s(idxs);
    % r(:,2,:) = y_s(idxs);
    % r(:,1,:) = x_s(idxs);
    % 
    % r0(:,3,:) = z0(idxn);
    % r0(:,2,:) = y0(idxn);
    % r0(:,1,:) = x0(idxn);
    % 
    % u0(:,3,:) = u0z(idxn);
    % u0(:,2,:) = u0y(idxn);
    % u0(:,1,:) = u0x(idxn);
    % u0_n = repmat(sqrt(sum(u0.^2,2)),1,3,1);
    % u0 = u0./u0_n;
    % 
    % i0 = reshape(i0_coils(idxn),n_samples,1,n_coils);
    % a0 = reshape(a0_coils(idxn),n_samples,1,n_coils);

    mu0 = 1.25663706212e-6;

    n_samples = length(x_s);
    n_coils = size(r0_coils,1);
    
    r = repmat([x_s,y_s,z_s],1,1,n_coils);

    r0 = repmat(reshape(r0_coils',1,3,size(r0_coils,1)),n_samples,1,1);

    u0 = repmat(reshape((u0_coils./vecnorm(u0_coils,2,2))',...
        1,3,size(u0_coils,1)),n_samples,1,1);

    i0 = repmat(reshape(i0_coils,1,1,length(i0_coils)),n_samples,1,1);
    a0 = repmat(reshape(a0_coils,1,1,length(a0_coils)),n_samples,1,1);
    
    r1 = r - r0;
    z = sum(r1.*u0,2);
    z_calc = z;
    rho_v = r1 - z.*u0;
    rho = sqrt(sum(rho_v.^2,2));
    rho_u = rho_v./rho;
    rho_u(isnan(rho_u)) = 0;
    
    alpha2 = a0.^2 + rho.^2 + z.^2 - 2*a0.*rho;
    beta2 = a0.^2 + rho.^2 + z.^2 + 2*a0.*rho;
    m = 1 - alpha2./beta2;
    C = mu0*i0/pi;
    
    [K,E] = ellipke(m);
    
    B_rho = C.*z./(2*alpha2.*sqrt(beta2).*rho).*...
        ((a0.^2 + rho.^2 + z.^2).*E - alpha2.*K);
    B_rho(isnan(B_rho)) = 0;
    B_z = C./(2*alpha2.*sqrt(beta2)).*...
        ((a0.^2 - rho.^2 - z.^2).*E + alpha2.*K);
    
    B_v = squeeze(sum(B_rho.*rho_u + B_z.*u0,3));
    B = sqrt(sum(B_v.^2,2));
    
    switch method
        case 'list'
            x = x_s;
            y = y_s;
            z = z_s;
        case 'meshgrid'
            x = reshape(x_s,meshsize);
            y = reshape(y_s,meshsize);
            z = reshape(z_s,meshsize);
            B_v = reshape(B_v,[meshsize,3]);
            B = reshape(B,meshsize);
    end
end

