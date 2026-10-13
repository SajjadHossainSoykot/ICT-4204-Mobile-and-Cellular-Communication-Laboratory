%% EXP08 - Cell Coverage, Radius and Cell Splitting
% Figure 1: Coverage area vs cell radius (circle and hexagon)
% Figure 2: Before/after splitting (one large cell, seven small cells)
clear; clc; close all;

%% 1. Parameters and calculations
R = 1;                  % Original cell radius (km)
r = 0.35*R;             % Small cell radius (km)
n = 4;                  % Path-loss exponent

Ac0 = pi*R^2;                   % Old circular area
Ac1 = pi*r^2;                   % New circular area
Ah0 = 3*sqrt(3)*R^2/2;         % Old hexagonal area
Ah1 = 3*sqrt(3)*r^2/2;         % New hexagonal area
P = (r/R)^n;                    % New/old transmitter power

d = sqrt(3)*r;                 % Adjacent small-cell center spacing
fprintf('Old radius R = %.2f km, small radius r = %.2f km\n', R, r);
fprintf('Circle: old = %.3f, small = %.3f km^2\n', Ac0, Ac1);
fprintf('Hexagon: old = %.3f, small = %.3f km^2\n', Ah0, Ah1);
fprintf('Area ratio = %.4f (%.2f%%)\n', (r/R)^2, 100*(r/R)^2);
fprintf('Power ratio = %.5f (%.2f dB)\n', P, 10*log10(P));
fprintf('Small-cell center spacing = %.3f km\n', d);

%% 2. Figure 1 - Coverage area vs cell radius
rv = linspace(0, 2*R, 200);
Ac = pi*rv.^2;                  % Circular area curve
Ah = 3*sqrt(3)*rv.^2/2;       % Hexagonal area curve

figure('Color','w','Position',[100 100 850 500]);
plot(rv,Ac,'b-','LineWidth',2); hold on;
plot(rv,Ah,'m--','LineWidth',2);
plot(R,Ah0,'ko','MarkerFaceColor','k');
plot(r,Ah1,'ks','MarkerFaceColor','k');
text(R+0.06,Ah0,'Original R','FontSize',10);
text(r+0.06,Ah1,'Small r','FontSize',10);
xlabel('Cell radius (km)'); ylabel('Coverage area (km^2)');
title('Cell Coverage Area vs Radius');
legend('Circular area','Hexagonal area','Location','northwest');
grid on; box on; hold off;

%% 3. Figure 2 - Before and after cell splitting
t = (30:60:390)*pi/180;          % Hexagon vertices + closing point
xy = [0 0; d 0; d/2 1.5*r; -d/2 1.5*r; ...
     -d 0; -d/2 -1.5*r; d/2 -1.5*r];

figure('Color','w','Position',[100 100 1100 510]);

% Before: one large hexagonal cell
subplot(1,2,1); hold on;
fill(R*cos(t),R*sin(t),[0.87 0.89 0.93], ...
     'EdgeColor','k','LineWidth',1.7);
plot(0,0,'k^','MarkerFaceColor','k','MarkerSize',9); % Base station
plot([0 R*cos(t(1))],[0 R*sin(t(1))],'b-','LineWidth',2);
text(0.45*R,0.33*R,'R','Color','b','FontWeight','bold');
title('Before Splitting: One Large Cell');
axis equal; grid on; box on;
xlim(1.3*[-R R]); ylim(1.3*[-R R]);
xlabel('Distance (km)'); ylabel('Distance (km)'); hold off;

% After: 1 center cell and 6 surrounding small cells
subplot(1,2,2); hold on;
for k = 1:7
     x = xy(k,1); y = xy(k,2);
     col = [0.91 0.91 0.91];
     if k == 1, col = [0.72 0.84 1]; end
     fill(x+r*cos(t),y+r*sin(t),col, ...
          'EdgeColor','k','LineWidth',1.2);
     plot(x,y,'k^','MarkerFaceColor','k','MarkerSize',5);
     text(x,y-0.45*r,sprintf('C%d',k), ...
          'HorizontalAlignment','center','FontSize',8);
end
% Mark the radius of small cell C2
x = xy(2,1); y = xy(2,2);
plot([x x+r*cos(t(1))],[y y+r*sin(t(1))],'b-','LineWidth',2);
text(x+0.4*r,y+0.37*r,'r','Color','b','FontWeight','bold');
% Dashed old boundary is a reference, NOT a perfect partition
h = plot(R*cos(t),R*sin(t),'k--','LineWidth',1.5);
legend(h,'Old cell boundary','Location','southoutside');
title('After Splitting: Seven Small Cells (Schematic)');
axis equal; grid on; box on;
xlim(1.3*[-R R]); ylim(1.3*[-R R]);
xlabel('Distance (km)'); ylabel('Distance (km)'); hold off;