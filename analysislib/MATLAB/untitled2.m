clear
% close all
clc
% close all

% x0 = 1;
% x1 = 1.01;
% 
% d = (x1-x0)/x0;
% mm = 2.8987*d.^(-.7043)+.3663;
% m0 = calc_m0(x0,x1,true,mm/3,mm*(3+3/(d/.01)),0.03*mm,200,100);


x0 = 1;
x1 = 1+logspace(-2,2,50);

for ii = 1:length(x1)
    d(ii) = (x1(ii)-x0)/x0;
    mm(ii) = 2.3565*d(ii)^(-0.9952)+0.7753;
    % m0(ii) = calc_m0(x0,x1(ii),true,.1+d(ii)^(1/10)*0.1,3/d(ii)^(1/2)*4,0.03,500,500);
    m0(ii) = calc_m0(x0,x1(ii),true,mm(ii)/3,mm(ii)*3,0.3*mm(ii),0.01*mm(ii),200,200,500);
end
d2=(x1-x0)./((x1+x0)/2);

[xData, yData] = prepareCurveData( d, log10(m0) );

ft = fittype( 'log10(a*(x)^(-b)+c)', 'independent', 'x', 'dependent', 'y' );
opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
opts.Display = 'Off';
opts.StartPoint = [2.3,1,.8];

[fitresult, gof] = fit( xData, yData, ft, opts );

figure(3)
subplot(2,1,1)
y1 = log10(m0);
y2 = transpose(fitresult(d));
semilogx(d,y1,d,y2)

subplot(2,1,2)
semilogx(d,y2-y1)

coeffvalues(fitresult)
diff(confint(fitresult),1)/4

figure(4)
subplot(2,1,1)
loglog(d,m0,d,transpose(fitresult(d)))

testfit.a = log(10);
testfit.b = 1;
testfit.c = 1/sqrt(2);

subplot(2,1,2)
loglog(d,abs(m0-testfunc(d,testfit)))

% [x_0,dx] = meshgrid(logspace(0,2,5)-.5,logspace(0,2,5));
% 
% m0 = zeros(size(x_0));
% 
% for ii = 1:size(x_0,1)
%     for jj = 1:size(x_0,2)
%         if ii==1 && jj==1
%             m0(ii,jj) = calc_m0(x_0(ii,jj),x_0(ii,jj) + dx(ii,jj),true);
%         else
%             m0(ii,jj) = calc_m0(x_0(ii,jj),x_0(ii,jj) + dx(ii,jj),false);
%         end
%     end
%     %clc
%     %disp(num2str(ii/size(x_0,1)*100,'%1.2f'))
% end
% imagesc(m0)

function y = testfunc(x,fit)
    y = fit.a*x.^(-fit.b)+fit.c;
end

function m0 = calc_m0(x_min,x_max,plotOutput,m_min,m_max,dm1,dm2,n1,n2,n3)
    if plotOutput
        m2 = calc_m0_single(x_min,x_max,3,linspace(m_min,m_max,n1));
        m1 = calc_m0_single(x_min,x_max,1,linspace(m2-dm2,m2+dm2,n2));
        m0 = calc_m0_single(x_min,x_max,2,linspace(m1-dm1,m1+dm1,n3));
    else
        m2 = calc_m0_single(x_min,x_max,0,linspace(m_min,m_max,n1));
        m1 = calc_m0_single(x_min,x_max,0,linspace(m2-dm2,m2+dm2,n2));
        m0 = calc_m0_single(x_min,x_max,0,linspace(m1-dm1,m1+dm1,n3));
    end
end

function m0 = calc_m0_single(x_min,x_max,figNumber,m)
dy = zeros(size(m));
for ii = 1:length(m)
    dy(ii) = testm(m(ii),x_min,x_max);
end

m1 = m;%(dy<=.01);
dy1 = dy;%(dy<=.01);
ddy = diff(dy1);
dddy = abs(diff(ddy));
ddddy = abs(diff(dddy));

[~,idx_sort] = sort(ddddy);
idx_sort(end-2:end);
idx_transition = sort(idx_sort(end-2:end));
if any(diff(idx_transition)>1)
    idx3 = idx_transition(3)+2;
else
    idx3 = idx_transition(2)+2;
end
y3 = [dy1(1:idx3-1),-dy1(idx3:end)];

m_sample = linspace(min(m1),max(m1),1e6+1);
y_fit = interp1(m1,y3,m_sample,'cubic');
m0 = mean(m_sample(abs(y_fit)==min(abs(y_fit))));
y_flip = interp1(m1,y3,m0,'cubic');

if figNumber > 0
    figure(figNumber)
    plot(m1,dy1,'.',m1,y3,'-k',m0,y_flip,'or')
    drawnow
    % set(gcf,"Position",get(gcf,"Position") + [600*(figNumber-1),0,0,0])
end

end


function dy = testm(m0,x_min,x_max)

% x_min = x_bar-dx/2;
% 
% x_max = x_bar+dx/2;

m = (x_max - x_min)*m0;
x = linspace(x_min,x_max,100001);
y = log10(linspace(10^(min(x)/m),10^(max(x)/m),length(x)))*m;
y_fit = polyval(polyfit(log(x),y,1),log(x));

dy = sqrt(sum((y_fit-y).^2))/sqrt(length(x));
% semilogx(x,y,x,y_fit-y,'.');
end