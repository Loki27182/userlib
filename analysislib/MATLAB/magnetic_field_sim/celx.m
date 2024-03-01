function [c,n] = celx(m)

nout = nargout==2;

if isempty(m)
    c = [];
    if nout
        n = [];
    end
    return
end

sz = size(m);
m = reshape(m,[],1);

if any(~isreal(m)) || any(m<0) || any(m>1) 
    error('All m must be real and between 0 and 1')
end

srted = issorted(m);
if ~srted
    [m,idx2] = sort(m);
end

qc = sqrt(1-m);
p = 1+qc;
g = ones(size(m));
cc = m.*m;
ss = 2*cc.*(qc./(qc+1));
em = p;
kk = qc;
jj = 0;

if nout
    n = zeros(sz);
end

completed = qc==0;
if ~isempty(completed)
        cc(completed) = 2;
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