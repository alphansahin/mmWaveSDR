function fcn_plotGroup(group,figNum, xValues)

figure(figNum)
fields = fieldnames(group);
Nsub = numel(fields);

if nargin == 2
    xValues = [1:numel(group.(fields{1}))];
end
for indSub = 1:Nsub
    subplot(Nsub,1,indSub)
    plot(xValues, group.(fields{indSub}), 'DisplayName',fields{indSub} )
    hold on
    grid on
    legend('show')
    a = max(abs(double(group.(fields{indSub}))))*1.1+0.001;
    b = min(abs(double(group.(fields{indSub}))));
    ylim([b a])
end
set(gcf,'Position',[108,323,2234,727]);