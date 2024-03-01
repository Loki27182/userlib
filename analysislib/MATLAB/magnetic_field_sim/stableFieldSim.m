function [B,B_v,xm,ym,zm] = stableFieldSim(x,y,z,r0_coils,u0_coils,i0_coils,a0_coils,method)
    arguments
        x (:,1) double {mustBeReal,mustBeFinite,mustBeNonempty}
        y (:,1) double {mustBeReal,mustBeFinite,mustBeNonempty}
        z (:,1) double {mustBeReal,mustBeFinite,mustBeNonempty}
        r0_coils (:,3) double {mustBeReal,mustBeFinite,mustBeNonempty}
        u0_coils (:,3) double {mustBeReal,mustBeFinite,mustBeNonempty}
        i0_coils (:,1) double {mustBeReal,mustBeFinite,mustBeNonempty}
        a0_coils (:,1) double {mustBeReal,mustBeFinite,mustBeNonempty,...
            mustBePositive}
        method string {mustBeMember(method,{'list','meshgrid'})} = ...
            'meshgrid'
    end
    
    if ~isequal(size(r0_coils,1),size(u0_coils,1),...
            size(i0_coils,1),size(a0_coils,1))
        error(['All coil parameter lists must have '...
            'the same number of rows'])
    end
    
    switch method
        case 'list'
            if isequal(size(x),size(y),size(z))
                x_s = x;
                y_s = y;
                z_s = z;
            else
                error('For list method, all sample lists must be the same length')
            end
        case 'meshgrid'
            [x_s,y_s,z_s] = meshgrid(x,y,z);
            meshsize = size(x_s);
            x_s = x_s(:);
            y_s = y_s(:);
            z_s = z_s(:);
    end
    
    mu0 = 1.25663706212e-6;

    n_samples = length(x_s);
    n_coils = size(r0_coils,1);
    
    r = repmat([x_s,y_s,z_s],1,1,n_coils);

    r0 = repmat(reshape(r0_coils',1,3,size(r0_coils,1)),n_samples,1,1);

    % u0 = repmat(reshape(u0_coils',1,3,size(u0_coils,1)),n_samples,1,1);
    % u0_n = sqrt(sum(u0.^2,2));
    % u0 = u0./u0_n;
    u0 = repmat(reshape((u0_coils./vecnorm(u0_coils,2,2))',...
        1,3,size(u0_coils,1)),n_samples,1,1);
    % isequal(u0,u1)
    
    
    i0 = repmat(reshape(i0_coils,1,1,length(i0_coils)),n_samples,1,1);
    a0 = repmat(reshape(a0_coils,1,1,length(a0_coils)),n_samples,1,1);
    
    r1 = r - r0;
    z = sum(r1.*u0,2);
    rho_v = r1 - z.*u0;
    rho = sqrt(sum(rho_v.^2,2));
    rho_u = rho_v./rho;
    rho_u(isnan(rho_u)) = 0;
    
    rho_ = rho./a0;
    z_ = z./a0;
        
    m = 4*rho_./(z_.^2 + (1 + rho_).^2);
    
    B0 = mu0*i0./(8*pi*a0);
    B1 = B0.*sqrt(m)./((1-m).*sqrt(rho_)); 
    
    sz_m = size(m);
    
    m = reshape(m,[],1);
    rho_ = reshape(rho_,[],1); 
    
    eps0 = sqrt(eps)/2;
    
    N = prod(sz_m);
    
    m = [m;m];
    rho_ = [rho_; Inf(N,1)];
    
    q2 = 1 - m;
    qc = sqrt(q2);
    p = 1 + qc; 
    g = ones(2*N,1);
    cc = m.*(m - (q2 + 1)./rho_);
    ss = 2*m.*qc.*(m./p - p./rho_); 
    em = p;
    kk = qc; 
    jj = 0;
    
    idx_done = find(qc == 0);
    if ~isempty(idx_done)
        cc(idx_done) = 2*(1 - 1./rho_(idx_done));
        p(idx_done) = pi;
        kk(idx_done) = 0;
        qc(idx_done) = 0;
        ss(idx_done) = 0;
        g(idx_done) = 1;
        em(idx_done) = 1;
    end
    
    idx_done = find(m == 0);
    if ~isempty(idx_done)
        cc(idx_done) = 0;
        p(idx_done) = 1;
        kk(idx_done) = 0;
        qc(idx_done) = 0;
        ss(idx_done) = 0;
        g(idx_done) = 1;
        em(idx_done) = 1;
    end
    
    while any(qc)
        qc = 2*sqrt(kk);
        kk = qc.*em;
        f = cc;
        cc = cc + ss./p;
        g = kk./p;
        ss = 2*(ss + f.*g);
        p = p + g;
        g = em;
        em = em + qc; 
        jj = jj + 1;
        
        idx_done = find(abs(g - qc) < g*eps0);
        
        if ~isempty(idx_done)
            cc(idx_done) = ss(idx_done) +...
                cc(idx_done).*em(idx_done);
            p(idx_done) = em(idx_done) .*...
                (em(idx_done) + p(idx_done));
            kk(idx_done) = 0;
            qc(idx_done) = 0;
            ss(idx_done) = 0;
            g(idx_done) = 1;
            em(idx_done) = 1;
        end
    end
    
    cel = pi*cc./(2*p);
    
    celxx = reshape(cel(1:N),sz_m);
    celx = reshape(cel(1+N:2*N),sz_m); 
    

    rho_ = reshape(rho_(1:N),sz_m);
    
    B_rho = B1.*z_.*celx./rho_;
    B_z = -B1.*celxx; 
    
    B_rho(rho_ == 0) = 0;
    B_rho(rho_ == 1 & z_ == 0) = 0;
    
    B_z(rho_ == 0) = B0(rho_ == 0)./...
        (4*pi*(z_(rho_ == 0).^2+1).^(3/2));
    B_z(rho_ == 1 & z_ == 0) = 0;
    
    B_v = squeeze(sum(B_rho.*rho_u + B_z.*u0,3));
    B = sqrt(sum(B_v.^2,2));
    
    switch method
        case 'list'
            xm = x_s;
            ym = y_s;
            zm = z_s;
        case 'meshgrid'
            xm = reshape(x_s,meshsize);
            ym = reshape(y_s,meshsize);
            zm = reshape(z_s,meshsize);
            B_v = reshape(B_v,[meshsize,3]);
            B = reshape(B,meshsize);
    end
end

