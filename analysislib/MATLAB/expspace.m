function [x,xlin] = expspace(xmin,xmax,n,inputForm)
    arguments 
        xmin (1,1) double {mustBePositive}
        xmax (1,1) double {mustBePositive}
        n (1,1) int64 ...
            {mustBeGreaterThanOrEqual(n,2)}
        inputForm (1,:) string {mustBeMember(inputForm,{'Normal','Exponent'})} = 'Normal'
    end
    if strcmp(inputForm,'Exponent')
        xmin = 10^xmin; 
        xmax = 10^xmax;
    end
    c = (xmax-xmin)/log10(xmax/xmin); 
    a = xmin*10^(-xmin/c); 
    xlin = linspace(xmin,xmax,n); 
    x = c*log10(xlin/a);
end