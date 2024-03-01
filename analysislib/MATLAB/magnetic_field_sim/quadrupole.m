clear

ngrid = 21;
xrange = [-1,1];
yrange = [0,1];
zrange = [-1,1];

x0 = [0,0];
y0 = [0,0];
z0 = [-.5,.5];
ux0 = [0,0];
uy0 = [0,0];
uz0 = [1,-1];
i0 = [1,1];
a0 = [.5,.5];

span = max([diff(xrange),diff(yrange),diff(zrange)]);
dx = span/ngrid;
r0 = [x0',y0',z0'];
u0 = [ux0',uy0',uz0'];
nmid = floor((ngrid+1)/2);
[x,y,z] = meshgrid(xrange(1):dx:xrange(2),...
    yrange(1):dx:yrange(2),...
    zrange(1):dx:zrange(2));
x = x(:);
y = y(:);
z = z(:);

bmax = dx/2;

[B,Bv] = fieldSim(x,y,z,r0,u0,i0,a0,'list');
Bv = Bv*1e6/ngrid;
B = B*1e6/ngrid;
m = B>bmax;
Bv(m,:) = Bv(m,:)./B(m)*bmax;

q = quiver3(x,y,z,Bv(:,1),Bv(:,2),Bv(:,3),'LineWidth',2 ,'AutoScale','off');
xlim([xrange(1)-span/10,xrange(2)+span/10])
xlim([yrange(1)-span/10,yrange(2)+span/10])
xlim([zrange(1)-span/10,zrange(2)+span/10])
axis equal
grid on
xlabel('X (m)')
ylabel('Y (m)')
zlabel('Z (m)')
