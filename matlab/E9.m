
%% EXP09 - Cellular Traffic and Erlang-B Analysis
clear; clc; close all;

% 1) Input parameters
A = 78.3;          % Offered traffic (Erlangs)
N = 90;            % Number of traffic channels
T = 100;           % Average call duration (seconds)
GoS = 0.02;        % Target Grade of Service (2%)

% 2) Calculate Erlang-B blocking probability
B = erlang_b(A, N);
Ac = A * (1 - B);  % Carried traffic
Ab = A * B;        % Blocked traffic

fprintf('Offered traffic      : %.2f Erlangs\n', A);
fprintf('Number of channels   : %d\n', N);
fprintf('Blocking probability : %.6f\n', B);
fprintf('Blocking percentage  : %.3f%%\n', B*100);
fprintf('Carried traffic      : %.3f Erlangs\n', Ac);
fprintf('Blocked traffic      : %.3f Erlangs\n', Ab);

% 3) Calculate calls per hour
Q = 3600 * A / T;

fprintf('\nAverage holding time : %.0f seconds\n', T);
fprintf('Calls per hour       : %.1f (approx. %d)\n', Q, round(Q));

% 4) Graph 1: Blocking probability vs offered traffic
traffic = linspace(1, 120, 300);
sets = [60 75 90 105];

figure('Color', 'w');
hold on;

for n = sets
    block = arrayfun(@(a) erlang_b(a, n), traffic);
    plot(traffic, block, 'LineWidth', 1.5, ...
        'DisplayName', sprintf('%d channels', n));
end

xlabel('Offered Traffic (Erlangs)');
ylabel('Blocking Probability');
title('Erlang-B Blocking Probability vs Offered Traffic');
legend('Location', 'best');
grid on;
hold off;

% 5) Find minimum channels for target GoS
minN = NaN;

for n = 1:500
    if erlang_b(A, n) <= GoS
        minN = n;
        break;
    end
end

fprintf('\nTarget GoS           : %.2f%%\n', GoS*100);
fprintf('Minimum channels     : %d\n', minN);

% 6) Graph 2: Blocking probability vs channel capacity
Nc = 70:110;
Bc = arrayfun(@(n) erlang_b(A, n), Nc);

figure('Color', 'w');
plot(Nc, Bc, '-o', 'LineWidth', 1.5);
hold on;

plot([Nc(1) Nc(end)], [GoS GoS], 'r--', ...
    'LineWidth', 1.5);

xlabel('Number of Traffic Channels');
ylabel('Blocking Probability');
title(sprintf('Blocking vs Channel Capacity (A = %.1f Erlangs)', A));
legend('Blocking Probability', '2% GoS Target', ...
    'Location', 'best');
grid on;
hold off;

% 7) Erlang-B function
function B = erlang_b(A, N)
    B = 1;
    for n = 1:N
        B = (A * B) / (n + A * B);
    end
end
