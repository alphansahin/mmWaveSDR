clear all
close all
clc

rng(12)

Noversampling = 4; % odd number
Nrepetitions = 4;
Nsamples = 8;
Nbit = 12;
rho = 1;

% Actual waveform
[Ga, Gb] = fcn_golaySequenceWrapper(32, 0, 'Budisin');
sequenceOriginal = Ga;
sequenceWaveform = fcn_singleCarrier(rho, repmat(sequenceOriginal,Nrepetitions,1), Noversampling);
sequenceWaveform = sequenceWaveform/max(abs(sequenceWaveform));

% Correlator
sequenceOversampled = repmat(sequenceOriginal,1,Noversampling).';
sequenceOversampled = sequenceOversampled(:);
detectorSettings.Nsamples = Nsamples;
detectorSettings.NbitsSymbols = Nbit;
detectorSettings.sequenceBPSK = sequenceOversampled;
detectorSettings.Nrepetitions = Nrepetitions;

figure(2)
stem(15*Noversampling-3+[0:numel(sequenceOversampled)-1],sequenceOversampled)
hold on
plot(sequenceWaveform,'-x')
drawnow

if true
    warning on

    [dataRealIn, dataImagIn,testVector, simTime] = generateTestVector(sequenceWaveform, Nsamples, Nbit);

    
    slout = sim('detector.slx');
    plotGroup.xcorrOutput = getLogged(slout,'xcorrSquare');
    plotGroup.acorrOutput = getLogged(slout,'acorrSquare');
    plotGroup.rhoOutput = double(plotGroup.xcorrOutput)./double(plotGroup.acorrOutput)/numel(sequenceOversampled);
    plotGroup.rhoOutput(plotGroup.acorrOutput==0)= 0;
    plotGroup.detectedSync = getLogged(slout,'detectedSync');
    plotGroup.cntDetectedSingle = getLogged(slout,'cntDetectedSingle');
    plotGroup.cntDetectedRepeat = getLogged(slout,'cntDetectedRepeat');


    %% Checks
    fcn_plotGroup(plotGroup,1)

    dataIQ = double(dataRealIn)+1i*double(dataImagIn);
    xcorrOutput = conv(flipud((sequenceOversampled)),dataIQ).';
    xcorrOutputDown = downsample(xcorrOutput,Nsamples,Nsamples-1);

    acorrOutput = conv(ones(size(sequenceOversampled)),abs(dataIQ).^2).';
    acorrOutputDown = downsample(acorrOutput,Nsamples,Nsamples-1);


    Nfields = numel(fieldnames(plotGroup));
    subplot(Nfields,1,1)
    plot(abs(xcorrOutputDown).^2)

    subplot(Nfields,1,2)
    plot(abs(acorrOutputDown))

    subplot(Nfields,1,3)
    plot(abs(xcorrOutputDown).^2./acorrOutputDown/numel(sequenceOversampled));
    ylim([0 1])
end


function [dataRealIn, dataImagIn, testVector, simTime] = generateTestVector(sequenceWaveform, Nsamples, Nbit)
    simTime = 128*1;
    %
    dataRealIn = int16(100*randn(simTime*8,1));
    dataImagIn = int16(100*randn(simTime*8,1));



    
    packet = [sequenceWaveform-1i*sequenceWaveform; linspace(0,1,32).'];
    start = 23;
    len = numel(packet);
    dataRealIn(start+[0:len-1]) = int16((2^11-1)*real(packet));
    dataImagIn(start+[0:len-1]) = int16((2^11-1)*imag(packet));
    

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





