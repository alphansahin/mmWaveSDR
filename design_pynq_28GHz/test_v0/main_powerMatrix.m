clear all
close all 
clc


tcpPortCMDRX = tcpclient("192.168.10.5",8080);
tcpPortDATARX = tcpclient("192.168.10.5",8081);

tcpPortCMDTX = tcpclient("192.168.10.3",8080);
tcpPortDATATX = tcpclient("192.168.10.3",8081);

IQDataAnalyzerTX = objIQDataAnalyzer('fsample', 1536e6, ...
                                 'fcarrier', 0, ...
                                 'figurePositionsOption',2,...
                                 'figureLocationX', 525, ...
                                 'figureLocationY', 700, ...
                                 'figureName', 'TX waveform', ...
                                 'figureIndexStart', 1000 ...
                                 );

IQDataAnalyzerRX = objIQDataAnalyzer('fsample', 1536e6, ...
                                 'fcarrier', 0, ...
                                 'figurePositionsOption',2,...
                                 'figureLocationX', 1725, ...
                                 'figureLocationY', 700, ...
                                 'figureName', 'RX waveform', ...
                                 'figureIndexStart', 2000 ...
                                 );
% Set frequency
fc = 24e9;
write(tcpPortCMDRX,['setCarrierFrequency ' num2str(fc)],"uint8")
getTheResponse(tcpPortCMDRX);    

write(tcpPortCMDTX,['setCarrierFrequency ' num2str(fc)],"uint8")
getTheResponse(tcpPortCMDTX);    



%% Set TX/RX AWVs
if 1
    % Set RX AWVs
    version='2.0';
    [rxAWVs, txAWVs, angleRX, angleTX] = awvTable(fc, version);
    NawvRX = size(rxAWVs,1);
    NawvTX = size(txAWVs,1);
end

if 1    
    for beamRXIndex = 0:NawvRX-1
        Ishifters = uint16(rxAWVs(beamRXIndex+1,1:2:end));
        Qshifters = uint16(rxAWVs(beamRXIndex+1,2:2:end));
        IQshifters = typecast(swapbytes(Ishifters*64+Qshifters),'uint8');        
        write(tcpPortCMDRX,['setAWVRX ' num2str(beamRXIndex) ' ' num2str(IQshifters)],"uint8")
        getTheResponse(tcpPortCMDRX);

        if(0)
            write(tcpPortCMDRX,['getAWVRX ' num2str(beamRXIndex)],"uint8")
            getTheResponse(tcpPortCMDRX);
        end
    end



    for beamTXIndex = 0:NawvTX-1
        Ishifters = uint16(txAWVs(beamTXIndex+1,1:2:end));
        Qshifters = uint16(txAWVs(beamTXIndex+1,2:2:end));
        IQshifters = typecast(swapbytes(Ishifters*64+Qshifters),'uint8'); 
        write(tcpPortCMDTX,['setAWVTX ' num2str(beamTXIndex) ' ' num2str(IQshifters)],"uint8")
        getTheResponse(tcpPortCMDTX);  
        
        if(0)
            write(tcpPortCMDTX,['getAWVTX ' num2str(beamTXIndex)],"uint8")
            getTheResponse(tcpPortCMDTX); 
        end
    end
end

%% Set TX/RX gains
if 1 
    if(1)
        rx_gain_ctrl_bb1 = 0x00; % I[0:3]:[0,1,3,7,F]:-6:0 dB, 4 steps, Q[0:3]:[0,1,3,7,F]:-6:0 dB, 4 steps
        rx_gain_ctrl_bb2 = 0x00; % I[0:3]:[0,1,3,7,F]:-6:0 dB, 4 steps, Q[0:3]:[0,1,3,7,F]:-6:0 dB, 4 steps
        rx_gain_ctrl_bb3 = 0x11; % I[0:3]:[0-F]:0:6 dB, 16 steps, Q[0:3]:[0-F]:0:6 dB, 16 steps, 
        rx_gain_ctrl_bfrf = 0xAA;% this is the gain before RF mixer, [0:3,RF gain]: 0-15 dB, 16 steps, [4:7, BF gain]: 0-15 dB, 16 steps
        write(tcpPortCMDRX,['setGainRX ' num2str(rx_gain_ctrl_bb1) ' ' num2str(rx_gain_ctrl_bb1) ' ' num2str(rx_gain_ctrl_bb1) ' ' num2str(rx_gain_ctrl_bfrf)],"uint8")
        getTheResponse(tcpPortCMDRX);   
    end
    write(tcpPortCMDRX,['getGainRX'],"uint8")
    getTheResponse(tcpPortCMDRX);       

     
    if(1)
        tx_bb_gain = 0x00;% tx_ctrl bit 3 (BB Ibias set) = 0: 0x00  = 0 dB, 0x01  = 6 dB, 0x02  = 6 dB, 0x03  = 9.5 dB
                          % tx_ctrl bit 3 (BB Ibias set) = 1, 0x00  = 0 dB, 0x01  = 3.5 dB, 0x02  = 3.5 dB, 0x03  = 6 dB *
        tx_bb_phase = 0x00;
        tx_bb_iq_gain = 0x00; % this is the gain in BB, [0:3,I gain]: 0-6 dB, 16 steps, [4:7, Q gain]: 0-6 dB, 16 steps
        tx_bfrf_gain = 0x77; % this is the gain after RF mixer, [0:3,RF gain]: 0-15 dB, 16 steps, [4:7, BF gain]: 0-15 dB, 16
        write(tcpPortCMDTX,['setGainTX ' num2str(tx_bb_gain) ' ' num2str(tx_bb_phase) ' ' num2str(tx_bb_iq_gain) ' ' num2str(tx_bfrf_gain)],"uint8")
        getTheResponse(tcpPortCMDTX);       
    end
    write(tcpPortCMDTX,['getGainTX'],"uint8")
    getTheResponse(tcpPortCMDTX);      
end


%% Transmission parameters
Noversampling = 4;
Nrepeat = 4;
rho = 0.5;
[Ga, ~] = fcn_golaySequenceWrapper(32, 0, 'Budisin');
sequenceOriginal = [Ga];
[syncWavefrom, pulseShape] = fcn_singleCarrier(rho, repmat(sequenceOriginal,1,Nrepeat), Noversampling);

f = 10;
T = 1/f;
t = linspace(0,T,100);
payload1 = linspace(0,1,100).';

rho = 0.15;
Noversampling=2;
Nsymbol = 300;
randomSymbols = (2*randi([0,1],Nsymbol,1))-1+1i*((2*randi([0,1],Nsymbol,1))-1);
payload2 = fcn_singleCarrier(rho, randomSymbols, Noversampling);
IQdataTX = [syncWavefrom; zeros(1,100).' ; payload1; payload2];

IQDataAnalyzerTX(IQdataTX)


if 1
    % Set the RX behaviour
    write(tcpPortCMDRX,'setModeSiver RXen1_TXen0',"uint8")
    getTheResponse(tcpPortCMDRX);

    modeRX = 1; % 0: STR, 1: WTR
    numIQdataSamplesPerTransfer = 1000;
    write(tcpPortCMDRX,['setupReception' ' ' num2str(modeRX) ' ' num2str(numIQdataSamplesPerTransfer)],"uint8")
    getTheResponse(tcpPortCMDRX);

    % set the receiver enable flag
    flag = 1; %0: disable RX, 1: enable RX
    write(tcpPortCMDRX,['setTransferEnableRXFlag ' num2str(flag)],"uint8")
    getTheResponse(tcpPortCMDRX);

    % Set the TX behaviour
    write(tcpPortCMDTX,'setModeSiver RXen0_TXen1',"uint8")
    getTheResponse(tcpPortCMDTX);

    numIQdataSamples = numel(IQdataTX); % max. 2^18 IQ samples (the limit is due to the FIFO depth (2^18) in the FPGA)
    IQdataTX = IQdataTX/max(abs(IQdataTX));

    beamTXIndex = 0;
    beamRXIndex = 0;
    powerMatrix = -inf(NawvRX,NawvTX);
    figure(1)
    h = imagesc(powerMatrix);
    xlabel('TX index')
    ylabel('RX index')
    colorbar
    for indTransmission = 1:inf
        if beamRXIndex == 0 &&  beamTXIndex == 0
            powerMatrix = -inf(NawvRX,NawvTX);
            h.CData = powerMatrix;
        end
        beamTXIndex = mod(beamTXIndex+1,NawvTX);
        write(tcpPortCMDTX,['setBeamIndexTX ' num2str(beamTXIndex)],"uint8")
        getTheResponse(tcpPortCMDTX);


        if beamTXIndex == 0
            beamRXIndex = mod(beamRXIndex+1,NawvRX);
            write(tcpPortCMDRX,['setBeamIndexRX ' num2str(beamRXIndex)],"uint8")
            getTheResponse(tcpPortCMDRX);                
        end
       
        disp(['TX beam angle:' num2str(angleTX(beamTXIndex+1))])    
        disp(['RX beam angle:' num2str(angleRX(beamRXIndex+1))]) 


        write(tcpPortCMDTX,['transmitIQSamples ' num2str(numIQdataSamples)],"uint8")
        writeIQData(tcpPortDATATX, IQdataTX)
        response = getTheResponse(tcpPortCMDTX);
        
        % get # of available transfer to pull
        write(tcpPortCMDRX,'getNumberOfAvailableTransfers',"uint8")
        response = getTheResponse(tcpPortCMDRX);
        responseSplit = strsplit((response));
        numberOfAvailableTransfers = str2num(responseSplit{1});

        if numberOfAvailableTransfers>0
            numberOfTransfers = 1; % 1 transfer
            timeOut = 1; % seconds
            write(tcpPortCMDRX,['receiveIQSamples' ' ' num2str(numberOfTransfers) ' ' num2str(timeOut)],"uint8")
            response= getTheResponse(tcpPortCMDRX);
            if contains(response,'Success')
                IQdataRX = readIQData(tcpPortDATARX,numIQdataSamplesPerTransfer);
                IQDataAnalyzerRX(IQdataRX)

                P = 10*log10(mean(abs(IQdataRX(300:600))).^2);
                powerMatrix(beamRXIndex+1,beamTXIndex+1) = P;
                h.CData = powerMatrix;
                drawnow
            end
        else
            disp('Not received...')
        end
    end

    % Set the behaviour
    write(tcpPortCMDTX,'setModeSiver RXen0_TXen0',"uint8")
    getTheResponse(tcpPortCMDTX);

    write(tcpPortCMDRX,'setModeSiver RXen0_TXen0',"uint8")
    getTheResponse(tcpPortCMDRX);    
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
    %disp(response)
end