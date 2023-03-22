clear all
close all 
clc

tcpPortCMD = tcpclient("192.168.10.3",8080);
tcpPortDATA = tcpclient("192.168.10.3",8081);
IQDataAnalyzer = objIQDataAnalyzer('fsample', 1536e6, ...
                                 'fcarrier', 0, ...
                                 'figurePositionsOption',2,...
                                 'figureLocationX', 1725, ...
                                 'figureLocationY', 700, ...
                                 'figureName', 'RX waveform' ...
                                 );
if 1 % basic connection test
    % get FPGA filename
    write(tcpPortCMD,'getFGPABitStreamFileName',"uint8")
    getTheResponse(tcpPortCMD);

    % get Monitor registers
    write(tcpPortCMD,'getRegisters',"uint8")
    getTheResponse(tcpPortCMD);

    % Set frequency
    write(tcpPortCMD,['getCarrierFrequency'],"uint8")
    getTheResponse(tcpPortCMD);

    fc = 28e9;
    write(tcpPortCMD,['setCarrierFrequency ' num2str(fc)],"uint8")
    getTheResponse(tcpPortCMD);

    beamTXIndex = 1;
    awv = [0xaa, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x3F, 0x3F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0xbb];
    write(tcpPortCMD,['setAWVTX ' num2str(beamTXIndex) ' ' num2str(awv)],"uint8")
    getTheResponse(tcpPortCMD);  
    
    beamTXIndex = 1;
    write(tcpPortCMD,['getAWVTX ' num2str(beamTXIndex)],"uint8")
    getTheResponse(tcpPortCMD); 


    beamRXIndex = 1;
    awv = [0xcc, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x3F, 0x3F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0xbb];
    write(tcpPortCMD,['setAWVRX ' num2str(beamRXIndex) ' ' num2str(awv)],"uint8")
    getTheResponse(tcpPortCMD);  
    
    beamRXIndex = 1;
    write(tcpPortCMD,['getAWVRX ' num2str(beamRXIndex)],"uint8")
    getTheResponse(tcpPortCMD); 
    
end

if 0 % setup the reception
    % Set the behaviour
    write(tcpPortCMD,'setModeSiver RXen1_TXen0',"uint8")
    getTheResponse(tcpPortCMD);

    modeRX = 0; % 0: STR, 1: WTR
    numIQdataSamplesPerTransfer = 1000
    write(tcpPortCMD,['setupReception' ' ' num2str(modeRX) ' ' num2str(numIQdataSamplesPerTransfer)],"uint8")
    getTheResponse(tcpPortCMD);



    % set the receiver enable flag
    flag = 1; %0: disable RX, 1: enable RX
    write(tcpPortCMD,['setTransferEnableRXFlag ' num2str(flag)],"uint8")
    getTheResponse(tcpPortCMD);

    % receive the IQ samples
    while 1
        % get # of available transfer to pull
        write(tcpPortCMD,'getNumberOfAvailableTransfers',"uint8")
        response = getTheResponse(tcpPortCMD);

        responseSplit = strsplit((response));
        numberOfAvailableTransfers = num2str(responseSplit{1});
        if numberOfAvailableTransfers>0
            numberOfTransfers = 1; % 1 transfer
            timeOut = 5; % seconds
            write(tcpPortCMD,['receiveIQSamples' ' ' num2str(numberOfTransfers) ' ' num2str(timeOut)],"uint8")
            response= getTheResponse(tcpPortCMD);
            if contains(response,'Success')
                IQdata = readIQData(tcpPortDATA,numIQdataSamplesPerTransfer);
                IQDataAnalyzer(IQdata)
            end
        else
            disp('Not received...')
        end
        
    end

    % Set the behaviour
    write(tcpPortCMD,'setModeSiver RXen0_TXen0',"uint8")
    getTheResponse(tcpPortCMD);    
end






%% function for test
function writeIQData(tcpPortDATA, IQdata)
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

