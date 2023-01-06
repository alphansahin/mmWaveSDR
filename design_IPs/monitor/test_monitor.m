clear all
close all
clc

simTime = 100;


dataIn = 150*ones(simTime,1);


slout = sim('monitor.slx');

plotGroup.tready = getLogged(slout,'dataOut');


%% Checks
fcn_plotGroup(plotGroup,4)
