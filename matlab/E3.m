%% EXP03 - Frequency Allocation and Channel Assignment
clear; clc; close all;

% 1) Input: spectrum per direction, channel width and duplex spacing
B = 25;                  % Spectrum per direction (MHz)
bw = 200;                % Channel spacing (kHz)
f0 = 890;                % First uplink channel (MHz)
df = 45;                 % Downlink - uplink spacing (MHz)
i = 2; j = 1;            % Hexagonal reuse shifts
N = i^2 + i*j + j^2;    % Cluster size = 7

% 2) Allocate channels to the 7 cell groups (fixed assignment)
M = floor(B*1000/bw);                 % Number of paired channels
cnt = floor(M/N) + ((1:N) <= mod(M,N));
grp = repelem(1:N, cnt);             % Each channel's cell group
ul = f0 + (0:M-1)*bw/1000;          % Uplink frequencies (MHz)
dl = ul + df;                       % Downlink frequencies (MHz)
c = lines(N);                       % One color for each group

fprintf('Total paired channels: %d\n', M);
fprintf('Cluster size N = %d; reuse factor = 1/%d\n', N, N);
for k = 1:N
    fprintf('Group F%d: %d channels\n', k, cnt(k));
end

% 3) Four visualizations
figure('Color','w','Position',[100 100 1100 760]);

subplot(2,2,1);
scatter(ul,grp,18,c(grp,:),'filled');
yticks(1:N); grid on;
xlabel('Uplink frequency (MHz)'); ylabel('Cell group');
title('Frequency allocation');

subplot(2,2,2);
h = bar(cnt); h.FaceColor = 'flat'; h.CData = c;
xticks(1:N); grid on;
xlabel('Cell group'); ylabel('Number of channels');
title('Channels per cell');

subplot(2,2,3); hold on;
R = 1;                         % Cell radius (km), for drawing
t = (30:60:390)*pi/180;       % Six corners + closing corner
for a = -3:3
    for b = -3:3
        if max([abs(a),abs(b),abs(a+b)]) > 3
            continue;          % Keep a hexagonal cluster of cells
        end
        x = sqrt(3)*R*(a+b/2);
        y = 1.5*R*b;
        g = mod(3*a+b,N)+1;    % Repeating F1-F7 reuse groups
        fill(x+R*cos(t),y+R*sin(t),c(g,:), ...
            'EdgeColor','k','LineWidth',0.6);
        text(x,y,sprintf('F%d',g),'HorizontalAlignment','center', ...
            'FontSize',8);
    end
end
axis equal off;
title('Hexagonal frequency reuse (N = 7)');
hold off;

subplot(2,2,4);
scatter([ul dl],[ones(1,M) 2*ones(1,M)],18, ...
    [c(grp,:);c(grp,:)],'s','filled');
yticks([1 2]); yticklabels({'Uplink','Downlink'});
ylim([0.5 2.5]); grid on;
xlabel('Frequency (MHz)'); title('Uplink and downlink mapping');

% Note: This is an illustrative fixed channel plan, not a full
% interference-checked cellular network allocation.
