function [c,n] = celxx(rho,m)

nout = nargout==2;

if isempty(m)
    c = [];
    if nout
        n = [];
    end
    return
end

sz = size(m);
sz2 = size(rho);
if sz~=sz2
    error('rho and m must be the same size')
end
m = reshape(m,[],1);
rho = reshape(rho,[],1);

if any(~isreal(m)) || any(m<0) || any(m>1)
    error('All m must be real and between 0 and 1')
end
if any(~isreal(rho)) || any(rho<0)
    error('All rho must be real and non-negative')
end

srted = issorted(m);
if ~srted
    [m,idx2] = sort(m);
    rho = rho(idx2);
end

q2 = 1-m;
qc = sqrt(q2);
p = 1+qc;
g = ones(size(m));
cc = m.*(m - (1 + q2)./rho);
ss = 2*m.*qc.*(m./p - p./rho);
em = p;
kk = qc;
jj = 0;

if nout
    n = zeros(sz);
end

completed = qc==0;
if ~isempty(completed)
    cc(completed) = 2*(1-1./rho(completed));
    p(completed) = pi;
    em(completed) = 1;
    ss(completed) = 0;
    g(completed) = 1;
    kk(completed) = 0;
    if nout
        n(completed) = jj;
    end
end

eps0 = sqrt(eps);

while any(qc)
    qc = 2*sqrt(kk);
    kk = qc.*em;
    f = cc;
    cc = cc + ss./p;
    g = kk./p;
    ss = 2*(ss+f.*g);
    p = p + g;
    g = em;
    em = em+qc;

    completed = (abs(g-qc) < g*eps0);
    if ~isempty(completed)
        cc(completed) = ss(completed)+cc(completed).*em(completed);
        p(completed) = em(completed).*(em(completed) + p(completed));
        em(completed) = 1;
        ss(completed) = 0;
        g(completed) = 1;
        qc(completed) = 0;
        kk(completed) = 0;
        if nout
            n(completed) = jj;
        end
    end
    jj = jj + 1;
end

if ~srted
    c(idx2) = pi*cc./(2.*p);
    c = reshape(c,sz);
    if nout
        n(idx2) = n;
    end
else
    c = reshape(pi*cc./(2.*p),sz);
end
end