clear all
close all 
clc

tcpPortCMD = tcpclient("192.168.10.3",8080);
tcpPortDATA = tcpclient("192.168.10.3",8081);
IQDataAnalyzer = objIQDataAnalyzer('fsample', 1536e6, ...
                                 'fcarrier', 0, ...
                                 'figurePositionsOption',2,...
                                 'figureLocationX', 525, ...
                                 'figureLocationY', 700, ...
                                 'figureName', 'TX waveform' ...
                                 );
if 1 % basic connection test
    % get FPGA filename
    write(tcpPortCMD,'getFGPABitStreamFileName',"uint8")
    getTheResponse(tcpPortCMD);

    % get Monitor registers
    write(tcpPortCMD,'getRegisters',"uint8")
    getTheResponse(tcpPortCMD);
end

Noversampling = 4;
Nrepeat = 4;
rho = 0.5;
[Ga, ~] = fcn_golaySequenceWrapper(32, 0, 'Budisin');
sequenceOriginal = [Ga];
[syncWavefrom, pulseShape] = fcn_singleCarrier(rho, repmat(sequenceOriginal,1,Nrepeat), Noversampling);


f = 10;
T = 1/f;
t = linspace(0,T,100);
payload1 = linspace(0,1,100).'

rho = 0.1;
Noversampling=6;
Nsymbol = 100;
randomSymbols = sqrt(2)/2*(2*randi([0,1],Nsymbol,1)-1)-1+1i*(2*randi([0,1],Nsymbol,1)-1);
randomSymbols = (2*randi([0,1],Nsymbol,1))-1;
payload2 = fcn_singleCarrier(rho, randomSymbols, Noversampling);


IQdata = [syncWavefrom; zeros(1,100).' ; payload1; payload2];

IQDataAnalyzer(IQdata)

if 1
    % Set the behaviour
    write(tcpPortCMD,'setModeSiver RXen0_TXen1',"uint8")
    getTheResponse(tcpPortCMD);

    numIQdataSamples = numel(IQdata); % max. 2^18 IQ samples (the limit is due to the FIFO depth (2^18) in the FPGA)
    IQdata = IQdata/max(abs(IQdata));
    for indTransmission = 1:1
        write(tcpPortCMD,['transmitIQSamples ' num2str(numIQdataSamples)],"uint8")
        writeIQData(tcpPortDATA, IQdata)
        response = getTheResponse(tcpPortCMD);
    end

    % Set the behaviour
    write(tcpPortCMD,'setModeSiver RXen0_TXen0',"uint8")
    getTheResponse(tcpPortCMD);
    
end


%% function for test
function writeIQData(tcpPortDATA, IQdata)

    IQdata = IQdata(:).';
    IQdataInt = int16([real(IQdata) imag(IQdata)]*2^13);
    write(tcpPortDATA,IQdataInt,"int16")
end

function IQdata = readIQData(tcpPortDATA,numIQdataSamples)
    expectedNumberOfBytes = numIQdataSamples*4;
    while  tcpPortDATA.NumBytesAvailable < expectedNumberOfBytes
    end
    data = typecast(read(tcpPortDATA),"int16");
    dataIandQ=double(data)*2^-11;
    IQdata = dataIandQ(1:end/2)+1i*dataIandQ(end/2+1:end);
end


function response = getTheResponse(tcpPortCMD)
    while tcpPortCMD.NumBytesAvailable == 0
    end
    response=char(typecast(read(tcpPortCMD),"uint8"));
    disp(response)
end
