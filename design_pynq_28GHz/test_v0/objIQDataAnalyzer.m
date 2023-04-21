classdef objIQDataAnalyzer < matlab.System
    % untitled Add summary here
    %
    % This template includes the minimum set of functions required
    % to define a System object with discrete state.

    % Public, tunable properties
    properties
        fsample = 1
        fcarrier = 0
        showTimeDomainSignal = 1;
        hTimeDomainSignal
        showPowerSpectralDensity = 1;
        hPowerSpectralDensity
        showIQDiagram = 1;
        hIQDiagram
        showTimeDomainSignal3D = 1;
        hTimeDomainSignal3D

        figureIndexStart = 1000;
        figurePositionsOption = 2; %0: auto figure position is off, 1: auto figure position is on, 3: internal settings in analyzeIQdata.m
        figureName = 'Waveform';
        figureLocationX = 625
        figureLocationY = 550
    end


    methods
        function obj = objIQDataAnalyzer(varargin)
            setProperties(obj,nargin,varargin{:});
        end
    end    

    methods(Access = protected)
        function setupImpl(obj,IQdata)
            % Perform one-time calculations, such as computing constants
            switch obj.figurePositionsOption
                case 0
                    % do nothing
                case 1
                    set(0,'units','pixels')
                    screenSize = get(0,'ScreenSize');
                    screenHeight = screenSize(4);
                    screenWidth = screenSize(3);

                    lenRatio = 0.30;
                    width = round(min(screenHeight,screenWidth)*lenRatio);
                    height = width;
    
                    xStep = width+5;
                    yStep = height+90;
    
                    xrefRatio = 0.55;
                    yrefRatio = 0.5;
                    xref = round(screenWidth*xrefRatio);
                    yref = round(screenHeight*yrefRatio);
    
    
                    positionRef = [xref,yref,width,height];
                case 2
                    xref = obj.figureLocationX;
                    yref = obj.figureLocationY;

                    if(1)
                        set(0,'units','pixels')
                        screenSize = get(0,'ScreenSize');
                        screenHeight = screenSize(4);
                        screenWidth = screenSize(3);
                        lenRatio = 0.30;
                        width = round(min(screenHeight,screenWidth)*lenRatio);
                        height = width;      
                    else
                        width = 560;
                        height = 420;
                    end
                    positionRef = [xref,yref,width,height];
                    xStep = width+5;
                    yStep = height+90;                    
            end
    
            if (obj.showTimeDomainSignal)
                h = figure(obj.figureIndexStart+0);
                if obj.figurePositionsOption>0
                    h.Position = positionRef + [xStep*0,yStep*0,0,0];
                end
    
                subplot(2,1,1)
                obj.hTimeDomainSignal{1}=plot([0:numel(IQdata)-1]*1/obj.fsample/1e-6, real(IQdata(:)), 'displayname',obj.figureName);
                grid on
                hold on
                title('In-phase')
                xlabel('Time (\mus)')
                ylabel('Amplitude')
                legend('off')
                legend('show')
                legend('Location','Best')
                ylim([-1 1])
    
                subplot(2,1,2)
                obj.hTimeDomainSignal{2}=plot([0:numel(IQdata)-1]*1/obj.fsample/1e-6, imag(IQdata(:)), 'displayname',obj.figureName);
                grid on
                hold on
                title('Quadrature')
                xlabel('Time (\mus)')
                ylabel('Amplitude')
                legend('off')
                legend('show')
                legend('Location','Best')
                ylim([-1 1])
            end
            if(obj.showPowerSpectralDensity)
                h = figure(obj.figureIndexStart+1);
                [valLin,freqList]=pwelch(IQdata,[],[],[],obj.fsample, 'centered');
                flist = (freqList+obj.fcarrier)/1e9;
                obj.hPowerSpectralDensity{1}=plot(flist,10*log10(valLin), 'displayname', obj.figureName);
                grid on
                hold on
                if obj.figurePositionsOption>0
                    h.Position = positionRef + [xStep*1,yStep*0,0,0];
                end
                xlabel('Frequency (GHz)')
                ylabel('Power/frequency (dB/Hz)')
                title('Power spectral density')
                legend('off')
                legend('show')
                legend('Location','Best')
                xlim([min(flist) max(flist)])
                ylim([min(10*log10(valLin))-10 max(10*log10(valLin))+30])
            end
            if(obj.showIQDiagram)
                h = figure(obj.figureIndexStart+2);
                if norm(IQdata)>0
                    ave = sqrt(mean(maxk((abs(IQdata).^2),10)));
                    IQdataN = IQdata/ave;
                else
                    IQdataN = IQdata;
                    warning('IQdiagram: The power of the signal is 0. Signal is not normalized.')
                end
                obj.hIQDiagram{1} = plot(real(IQdataN),imag(IQdataN), 'displayname', obj.figureName);
                grid on
                hold on
                if obj.figurePositionsOption>0
                    h.Position = positionRef + [xStep*1,yStep*-1,0,0];
                end
                xlabel('In-phase')
                ylabel('Quadrature')
                legend('off')
                legend('show')
                legend('Location','Best')
                title('IQ diagram (Normalized)')
                drawnow
                maxVal = 1.2;
                xlim([-maxVal maxVal])
                ylim([-maxVal maxVal])
                axis('square')
            end
    
            if(obj.showTimeDomainSignal3D)
                h = figure(obj.figureIndexStart+3);
                t = [0:numel(IQdata)-1]*1/obj.fsample/1e-6;
                obj.hTimeDomainSignal3D{1} = plot3(t, real(IQdata),imag(IQdata), 'displayname', obj.figureName);
                grid on
                hold on
                if obj.figurePositionsOption>0
                    h.Position = positionRef + [xStep*0,yStep*-1,0,0];
                end
                xlabel('Time (\mus)')
                ylabel('In-phase')
                zlabel('Quadrature')
                legend('off')
                legend('show')
                legend('Location','Best')
                title('Time vs. IQ data')
                axis('equal')
                view(gca,[85 3]);
                drawnow
                maxVal = 1.2;
                ylim([-maxVal maxVal])
                zlim([-maxVal maxVal])
            end
            drawnow
        end

        function stepImpl(obj,IQdata)
            % Implement algorithm. Calculate y as a function of input u and
            % discrete states.
            if (obj.showTimeDomainSignal)
                obj.hTimeDomainSignal{1}.YData = real(IQdata);
                obj.hTimeDomainSignal{2}.YData = imag(IQdata);
            end

            if(obj.showPowerSpectralDensity)
                [valLin,~]=pwelch(IQdata,[],[],[],obj.fsample, 'centered');
                obj.hPowerSpectralDensity{1}.YData = 10*log10(valLin);
            end

            if norm(IQdata)>0
                ave = sqrt(mean(maxk((abs(IQdata).^2),10)));
                IQdataN = IQdata/ave;
            else
                IQdataN = IQdata;
                warning('IQdiagram: The power of the signal is 0. Signal is not normalized.')
            end

            if(obj.showIQDiagram)
                obj.hIQDiagram{1}.XData = real(IQdataN);
                obj.hIQDiagram{1}.YData = imag(IQdataN);
            end
    

            if(obj.showTimeDomainSignal3D)
                obj.hTimeDomainSignal3D{1}.YData = real(IQdata);
                obj.hTimeDomainSignal3D{1}.ZData = imag(IQdata);
            end
        end

        function resetImpl(obj)
            % Initialize / reset discrete-state properties
        end
    end
end
