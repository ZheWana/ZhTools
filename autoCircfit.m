% 功能：自动根据输入数据进行椭圆拟合，并画图，输出各轴bias
% 输入参数：可以是一个外部导入的Table，取首列作为x，第二列作为y;
%          可以是两个列向量，首列作为x，第二列作为y;
function [] = autoCircfit(varargin)
narginchk(1,2)

pren = size(varargin{1,1}(:,1));

if nargin == 1
    %% 单表参数
    % 取首列作为x，第二列作为y;
    % 检测并删除表中离群数据
    res=rmoutliers(varargin{1,1}(:,1:2));
elseif nargin == 2
    %% 逐列参数，合并为表
    % 首列作为x，第二列作为y;
    % 检测并删除表中离群数据
    res=rmoutliers(table(varargin{1,1},varargin{1,2}));
end

x = res(:,1);
y = res(:,2);

%% 数据类型验证与转换
if istable(x)
    x = table2array(x);
end

if istable(y)
    y = table2array(y);
end

%% 图形拟合计算
n=length(x);
xx=x.*x;
yy=y.*y;
xy=x.*y;
A=[sum(x) sum(y) n;sum(xy) sum(yy) sum(y);sum(xx) sum(xy) sum(x)];
B=[-sum(xx+yy) ; -sum(xx.*y+yy.*y) ; -sum(xx.*x+xy.*y)];
a=A\B;
xc = -.5*a(1);
yc = -.5*a(2);
R = sqrt((a(1)^2+a(2)^2)/4-a(3));

%% 绘制结果图像
scatter(x,y);
rectangle('Position',[xc-R,yc-R,2*R,2*R],'Curvature',[1,1],'linewidth',1),axis equal;
txt = sprintf('Del %.0f rows\nx=%.5f\ny=%.5f',(pren(1,1)-n),xc,yc);
text(xc,yc,txt,'FontSize',14);
end