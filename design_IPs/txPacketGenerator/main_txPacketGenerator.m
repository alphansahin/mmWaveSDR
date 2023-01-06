clear all
close all
clc


%% Checks
if true
    warning on
    [dataRealIn, dataImagIn,testVector, simTime] = generateTestVector;

    
    slout = sim('txPacketGenerator.slx');

    plotGroup.transferReady = getLogged(slout,'transferReady');

    %plotGroup.stdatare = getLogged(slout,'s_tdata_re');
    %plotGroup.stvalidre = getLogged(slout,'s_tvalid_re');

    %plotGroup.stdatare = getLogged(slout,'s_tdata_re');
    plotGroup.mtreadyre = getLogged(slout,'m_tready_re');
    plotGroup.stvalidre = getLogged(slout,'s_tvalid_re');    
    

    %plotGroup.mtdatare = getLogged(slout,'m_tdata_re');
    plotGroup.mtvalidre = getLogged(slout,'m_tvalid_re');
    plotGroup.streadyre = getLogged(slout,'s_tready_re');


    fcn_plotGroup(plotGroup,4)
end


function [dataRealIn, dataImagIn, testVector, simTime] = generateTestVector()
    simTime = 128;
    Nsamples = 8;
    %
    testVector.mode = ones(simTime,1);
    testVector.mode(100:end) = 0;

    %
    testVector.packetSize = 5*ones(simTime,1);

    %
    testVector.transferReady = zeros(simTime,1);
    testVector.transferReady(80) = 1;
    
    %
    testVector.s_tvalid_re = zeros(simTime,1);
    testVector.s_tvalid_re(88:end) = 1;

    %
    testVector.s_tvalid_im = zeros(simTime,1);    
    
    %
    testVector.m_tready_re = zeros(simTime,1);
    testVector.m_tready_re(100+[0:10]) = 1;
    %
    testVector.m_tready_im = zeros(simTime,1);    

    %
    dataRealIn = int16(100*ones(simTime*8,1));
    dataImagIn = int16(100*ones(simTime*8,1));



    dataRealInU = dataRealIn;
    dataRealInGroup = fliplr(reshape(dataRealInU,8,[]).')';
    dataRealInGroup = dec2hex(typecast(dataRealInGroup(:),'uint16'),4);
    dataRealInGroup = reshape(dataRealInGroup.',Nsamples*4,[]).';
    testVector.s_tdata_re = fi(zeros(size(dataRealInGroup,1),1),0,128,0);
    testVector.s_tdata_re.hex = dataRealInGroup;
    
    dataImagInU = dataImagIn;
    dataImagInGroup = fliplr(reshape(dataImagInU,8,[]).')';
    dataImagInGroup = dec2hex(typecast(dataImagInGroup(:),'uint16'),4);
    dataImagInGroup = reshape(dataImagInGroup.',Nsamples*4,[]).';
    testVector.s_tdata_im = fi(zeros(size(dataImagInGroup,1),1),0,128,0);
    testVector.s_tdata_im.hex = dataImagInGroup;

end
