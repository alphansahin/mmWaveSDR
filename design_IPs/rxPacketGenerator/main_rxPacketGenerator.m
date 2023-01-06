clear all
close all
clc

rng(12)

if true
    warning on

    [dataRealIn, dataImagIn,testVector, simTime] = generateTestVector();

    
    slout = sim('rxPacketGenerator.slx');
    plotGroup.detectedSync = getLogged(slout,'detectorTrigger');
    plotGroup.softTransferTrigger = getLogged(slout,'softTrigger');
    %plotGroup.stdatare = getLogged(slout,'s_tdata_re');
    plotGroup.mtreadyre = getLogged(slout,'m_tready_re');
    plotGroup.stvalidre = getLogged(slout,'s_tvalid_re');    
    

    %plotGroup.mtdatare = getLogged(slout,'m_tdata_re');
    plotGroup.mtvalidre = getLogged(slout,'m_tvalid_re');
    plotGroup.mtlastre = getLogged(slout,'m_tlast_re');
    plotGroup.streadyre = getLogged(slout,'s_tready_re');

    plotGroup.numberOfTransfers = getLogged(slout,'numberOfTransfers');
    plotGroup.nullNumberOfTransfersCounter = getLogged(slout,'resetNumberOfTransfersCounter');
    plotGroup.transfersEnable = getLogged(slout,'transfersEnable');

    %plotGroup.mtdataim = getLogged(slout,'m_tdata_im');
    %plotGroup.mtvalidim = getLogged(slout,'m_tvalid_im');
    %plotGroup.mtlastim = getLogged(slout,'m_tlast_im');
    %plotGroup.mtreadyim = getLogged(slout,'m_tready_im');

    %% Checks
    fcn_plotGroup(plotGroup,1)
end


function [dataRealIn, dataImagIn, testVector, simTime] = generateTestVector()
    simTime = 150*1;
    %
    testVector.mode = ones(simTime,1);
    testVector.mode(1:10) = 0;

    testVector.fifoCounter = 325*ones(simTime,1);
    testVector.stopCounter = 325*ones(simTime,1);

    %
    testVector.transferSize = 5     *ones(simTime,1);
    
    % 
    testVector.transferEnable = ones(simTime,1);


    % 
    testVector.resetNumberOfTransfersCounter = zeros(simTime,1); 

    %
    testVector.softTrigger = zeros(simTime,1);
    testVector.softTrigger(80:105) = 1;
    %testVector.softTrigger(107:110) = 1;

    %
    testVector.s_tvalid_re = ones(simTime,1);
    %testVector.s_tvalid_re(88) = 0;

    %
    testVector.s_tvalid_im = ones(simTime,1);    

    %
    testVector.detectorTrigger = zeros(simTime,1);   
    testVector.detectorTrigger(82) = 1;   

    testVector.detectorTrigger(100) = 1;   
    
    testVector.detectorTrigger(110) = 1;   

    testVector.detectorTrigger(120) = 1;       

    %
    testVector.m_tready_re = ones(simTime,1);
    %testVector.m_tready_re(85)= 0;
    %
    testVector.m_tready_im = ones(simTime,1);    

    %
    Nsamples = 8;
    dataRealIn = int16(100*randn(simTime*8,1));
    dataImagIn = int16(100*randn(simTime*8,1));



    start = 701;
    lenSin = 100;
    fc = 50e6;
    Ts = 1/1.536e9;    
    a = (1*cos([0:lenSin-1]'*2*pi*fc*Ts));
    b = -a;    
    packet = [a+1i*b];
    len = numel(packet);
    dataRealIn(start+[0:len-1]) = int16((2^11-1)*real(packet));
    dataImagIn(start+[0:len-1]) = int16((2^11-1)*imag(packet));
        


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






