%%%
% This script logs data from the Rigol spectrum analyzer. It needs to be
% set up for auto triggering, with a scan time less than dt below (probably
% best to have a bit of overhead as well), and frequency limits and number
% of points needs to be hard coded in until I figure out how to pull that
% data from the SA as well (currently it is only giving powers at each
% point without actually telling us what each point is). It shows the
% current SA data as it goes and picks out the peak (using a polyfit on the
% data, which is approximately quadratic on this logarithmic scale). It
% also plots a histogram of all center frequencies fitted this way for the
% logged duration, as well as a plot of the center frequency and power over
% time, and an Allen deviation curve for the frequency data. It saves the
% data as a .mat file, and saves the plots as a matlab figure and a png.

clear

% path = 'D:/misc/2024/01/08/drift_plots/';       % Today's misc datapath


% T = 1;                                         % Max duration of log
% name = 'short_test';                            % Root name of save files

% T = 10;
% name = 'local_terminated_10min';
% name = 'computer_terminated_10min';

% T = 60*15;
% name = 'overnight_run';

% path = 'D:/misc/2024/01/09/drift_plots/';
%
% T = 1;
% name = 'DDS_drift_short_test';

% T = 10;
% name = 'DDS_drift_medium_test';

% T = 1;
% name = 'program_test_0';

% T = 1;
% name = 'program_test_1';

% T = 19*60;
% name = 'program_test_2';

% T = 2;
% name = 'program_test_3';

% T = 60*19-11;
% name = 'DDS_overnight';

path = 'D:/misc/2024/01/11/drift_plots/';
% T = 10;
% name = 'DDS_test';

% T = 2*60;
% name = 'DDS_long_test';

T = 15*60;
name = 'DDS_overnight';

dt = .5;                            % Timestep - needs to be chosen so data logging doesn't back up (>0.3s works for initial testing settings)
saveData = true;                    % Save files or not
remoteSave = false;                  % Whether or not to copy saved files to google drive
plotContinuous = false;
timeout = 60;                       % Max timeout while waiting for SA to respond

f = linspace(79.95,80.01,601);      % Hard coded until I figure out how to pull this from the SA

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% You shouldn't have to adjust anything below here
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
pathName = [path name '/'];
if exist(pathName,'dir')~=7
    mkdir(pathName)
end
data = zeros(ceil(T*60/dt),601);
f_peak = zeros(1,size(data,1));
p_peak = zeros(1,size(data,1));
t = zeros(1,size(data,1));

rigol = visadev('Rigol_Spectrum_Analyzer');
data_ii = cellfun(@(x) str2double(x(1)),regexp(writeread(rigol,":TRACE:DATA? TRACE1"),'([+-]?\d*\.\d*)','tokens'))*10;

t0 = datetime('now');
t_delay = zeros(size(t));
termEarly = false;
tic

%try
    for ii = 1:size(data,1)
        t_delay(ii) = toc-ii*dt;
        if ii>1% && plotContinuous
            if ii==2
                fig8 = figure(8);
                plot(-t_delay(2:ii),'x')
                ylim([min([0,min(-t_delay(1:ii))*1.1]),max(-t_delay(1:ii))*1.1])
                drawnow
            else
                fig8.Children(1).Children(1).YData = -t_delay(2:ii);
                fig8.Children(1).Children(1).XData = 1:length(t_delay(2:ii));
                fig8.Children(1).YLim = [min([0,min(-t_delay(1:ii))*1.1]),max(-t_delay(1:ii))*1.1];
                drawnow
            end
        end
        while toc<ii*dt
        end
        t(ii) = toc-dt;
        if (ii>1 && t(ii) > dt*(ii-1)+timeout)
            disp('Logging got too backed up and quit early.')
            termEarly = true;
            ii = ii-1;
            break
        end
        data_ii = cellfun(@(x) str2double(x(1)),regexp(writeread(rigol,":TRACE:DATA? TRACE1"),'([+-]?\d*\.\d*)','tokens'))*10;
        data(ii,:) = data_ii;

        if plotContinuous
            f_fit = f(data_ii>-20);
            p = polyfit(f_fit,data_ii(data_ii>-20),2);
            f_peak_ii = -p(2)/(2*p(1));
            p_peak_ii = polyval(p,f_peak_ii);
            d_fit = polyval(p,f_fit);
            t_plot = t0 + t(1:ii)/3600/24;

            f_peak(ii) = f_peak_ii;
            p_peak(ii) = p_peak_ii;

            if ii==2
                fig7 = figure(7);
                set(gcf,'Position',[1930,130,1900,650])

                subplot(2,3,1)
                plot(f,data_ii,'-',f_fit,d_fit,'x',f_peak_ii,p_peak_ii,'o')
                xlabel('Frequency (MHz)')
                ylabel('Power (dBm)')
                title('Current Spectrum')

                subplot(2,3,2)
                imagesc(f,t_plot,data(1:ii,:))
                set(gca,'YDir','normal')
                xlabel('Frequency (MHz)')
                ylabel('Time (s)')
                cb = colorbar;
                ylabel(cb,'Power (dBm)','Interpreter','latex')
                title('Spectrum Log')

                subplot(2,3,6)
                plot(t_plot,p_peak(1:ii))
                xlabel('Time')
                ylabel('Center Peak Power (dBm)')
                title('Peak Power')

                subplot(2,3,4)
                plot(t_plot,f_peak(1:ii))
                xlabel('Time')
                ylabel('Center Frequency (MHz)')
                title('Peak Location')

                subplot(2,3,3)
                [N,edges] = histcounts(f_peak(1:ii),linspace(min(f_peak(1:ii)),max(f_peak(1:ii)),20));
                bar(edges(1:end-1) + mean(diff(edges))/2,N,1)
                xlabel('Center Frequency (MHz)')
                ylabel('Counts')
                title('Center Frequency Histogram')

                subplot(2,3,5)
                loglog([],[])
                xlabel('$\tau$ (min)')
                ylabel('$\sigma_\mathrm{f}(\tau)$ (kHz)')
                title('Center Frequency Allan Deviation')

            elseif ii>2
                fig7.Children(end).Children(end).XData = f;
                fig7.Children(end).Children(end).YData = data_ii;
                fig7.Children(end).Children(end-1).XData = f_fit;
                fig7.Children(end).Children(end-1).YData = d_fit;
                fig7.Children(end).Children(end-2).XData = f_peak_ii;
                fig7.Children(end).Children(end-2).YData = p_peak_ii;

                fig7.Children(end-1).Children(end).XData = f;
                fig7.Children(end-1).Children(end).YData = t_plot;
                fig7.Children(end-1).Children(end).CData = data(1:ii,:);
                fig7.Children(end-1).YLim = [min(t_plot),max(t_plot)];

                fig7.Children(end-3).Children(end).XData = t_plot;
                fig7.Children(end-3).Children(end).YData = p_peak(1:ii);

                fig7.Children(end-4).Children(end).XData = t_plot;
                fig7.Children(end-4).Children(end).YData = f_peak(1:ii);

                [N,edges] = histcounts(f_peak(1:ii),linspace(min(f_peak(1:ii)),max(f_peak(1:ii)),20));
                fig7.Children(end-5).Children(end).XData = edges(1:end-1) + mean(diff(edges))/2;
                fig7.Children(end-5).Children(end).YData = N;

                if ii>=10
                    m = unique(floor(logspace(0,log10((ii-1)/3),600)));
                    [avar,tau] = allanvar(f_peak(1:ii),m,1/mean(diff(t(1:ii))));
                    if ii==10
                        loglog(fig7.Children(end-6),tau/60,sqrt(avar)*1000)
                        xlabel(fig7.Children(end-6),'$\tau$ (min)')
                        ylabel(fig7.Children(end-6),'$\sigma_\mathrm{f}(\tau)$ (kHz)')
                        title(fig7.Children(end-6),'Center Frequency Allan Deviation')
                    else
                        fig7.Children(end-6).Children(end).XData = tau/60;
                        fig7.Children(end-6).Children(end).YData = sqrt(avar)*1000;
                        fig7.Children(end-6).XLim = [min(tau/60),max(tau/60)];
                        fig7.Children(end-6).YLim = [min(sqrt(avar)*1000)/10,max(sqrt(avar)*1000)*10];

                    end
                end
            end
            drawnow
        end
    end
    clear rigol

    ii_max = ii;

    if ~plotContinuous
        for ii = 1:ii_max
            f_fit = f(data(ii,:)'>-20);
            p = polyfit(f_fit,data(ii,data(ii,:)>-20),2);
            f_peak_ii = -p(2)/(2*p(1));
            p_peak_ii = polyval(p,f_peak_ii);
            d_fit = polyval(p,f_fit);
            t_plot = t0 + t(1:ii)/3600/24;

            f_peak(ii) = f_peak_ii;
            p_peak(ii) = p_peak_ii;
        end
    end

    if termEarly
        t = t(1:ii);
        f_peak = f_peak(1:ii_max);
        p_peak = p_peak(1:ii_max);
        data = data(1:ii_max,:);
        t_plot = t_plot(1:ii_max);
    end

    m = unique(floor(logspace(0,log10((ii-1)/2),600)));
    [avar,tau] = allanvar(f_peak,m,1/mean(diff(t)));

    if saveData
        save([pathName '/data.mat'])

        figure(1)
        plot(f,data_ii,'-',f_fit,d_fit,'x',f_peak_ii,p_peak_ii,'o')
        xlabel('Frequency (MHz)')
        ylabel('Power (dBm)')
        title('Sample Spectrum')
        xlim([min(f),max(f)])
        saveas(gcf,[pathName '/single_spectrum.png'])
        savefig(gcf,[pathName '/single_spectrum.fig'])

        figure(2)
        imagesc(f,t_plot,data)
        set(gca,'YDir','normal')
        xlabel('Frequency (MHz)')
        ylabel('Time (s)')
        cb = colorbar;
        ylabel(cb,'Power (dBm)','Interpreter','latex')
        title('Spectrum Log')
        saveas(gcf,[pathName '/full_log.png'])
        savefig(gcf,[pathName '/full_log.fig'])

        figure(3)
        histogram(f_peak,linspace(min(f_peak),max(f_peak),20))
        xlabel('Center Frequency (MHz)')
        ylabel('Counts')
        title('Center Frequency Histogram')
        saveas(gcf,[pathName '/histogram.png'])
        savefig(gcf,[pathName '/histogram.fig'])

        figure(5)
        loglog(tau/60,sqrt(avar)*1e6)
        xlabel('$\tau$ (min)')
        ylabel('$\sigma_\mathrm{f}(\tau)$ (Hz)')
        title('Center Frequency Allan Deviation')
        xlim([min(tau/60),max(tau/60)]);
        ylim([min(sqrt(avar)*1e6)/2,max(sqrt(avar)*1e6)*2]);
        saveas(gcf,[pathName '/adev.png'])
        savefig(gcf,[pathName '/adev.fig'])

        %time_delay = get(figure(8).Children(1).Children(1),'YData');
        t_cal = t_plot(diff(t_delay)<min(diff(t_delay))/2);
        t_cal_plot = [t_cal;t_cal;NaT(1,length(t_cal))];
        t_cal_plot = t_cal_plot(:);

        figure(6)
        p_min_plot = mean(p_peak)-(max(p_peak)-min(p_peak))*.6;
        p_max_plot = mean(p_peak)+(max(p_peak)-min(p_peak))*.6;
        plot(t_plot,p_peak,t_cal_plot',repmat([p_min_plot,p_max_plot,NaN],1,length(t_cal_plot)/3),':k')
        xlabel('Time')
        ylabel('Center Peak Power (dBm)')
        title('Peak Power')
        xlim([min(t_plot),max(t_plot)])
        ylim([p_min_plot,p_max_plot])
        legend('Data','Times of SA delay')
        saveas(gcf,[pathName '/peak_power.png'])
        savefig(gcf,[pathName '/peak_power.fig'])

        figure(4)
        f_plot = (f_peak - mean(f_peak))*1e6;
        f_min_plot = mean(f_plot)-(max(f_plot)-min(f_plot))*.6;
        f_max_plot = mean(f_plot)+(max(f_plot)-min(f_plot))*.6;
        n_smooth = mean(tau(sqrt(avar)==min(sqrt(avar))));
        plot(t_plot,smooth(f_plot,n_smooth),t_cal_plot',repmat([f_min_plot,f_max_plot,NaN],1,length(t_cal_plot)/3),':k')
        xlabel('Time')
        ylabel('$\Delta f$ (Hz from mean)')
        title('Peak Frequency Variation')
        xlim([min(t_plot),max(t_plot)])
        ylim([f_min_plot,f_max_plot])
        saveas(gcf,[pathName '/peak_location.png'])
        savefig(gcf,[pathName '/peak_location.fig'])

        figure(9)
        loglog(tau/60,sqrt(avar)*1e6/(mean(f_peak)*1e6)*1e9)
        xlabel('$\tau$ (min)')
        ylabel('$\sigma_\mathrm{f}(\tau)$ (ppb)')
        title('Center Frequency Allan Deviation')
        xlim([min(tau/60),max(tau/60)]);
        ylim([min(sqrt(avar)*1e6/(mean(f_peak)*1e6)*1e9)/2,max(sqrt(avar)*1e6/(mean(f_peak)*1e6)*1e9)*2]);
        saveas(gcf,[pathName '/adev_bbp.png'])
        savefig(gcf,[pathName '/adev_bbp.fig'])
%%
        figure(11)
        [pxx,f_p] = periodogram((f_peak - mean(f_peak))*1e6,[],[],1/mean(seconds(diff(t_plot))));
        pxx = pxx(2:end);
        f_p = f_p(2:end);
        pxx_log = 10*log10(pxx);
        n_sm_0 = 1;
        n_sm_f = 500;
        n_sm = floor(expspace(n_sm_0,n_sm_f,length(pxx)));

        pxx_sm = zeros(size(pxx));
        for ii = 1:length(pxx)
            df = n_sm(ii);

            idx_0 = ii - floor((n_sm(ii) - 1)/2);
            idx_f = ii + ceil((n_sm(ii) - 1)/2);
            if idx_0 >= 1 && idx_f <= length(pxx)
                pxx_sm(ii) = mean(pxx(idx_0:idx_f));
            elseif idx_0 <= 0
                if idx_f > length(pxx)
                    error('Smoothing bin wider than span')
                end
                pxx_sm(ii) = mean([flipud(pxx(1:(1-idx_0))); pxx(1:idx_f)]);
            elseif idx_0 >length(pxx)
                if 2*length(pxx)-idx_f+1 <= 0
                    error('Smoothing bin wider than span')
                end
                pxx_sm(ii) = mean([pxx(idx_0:length(pxx));flipud(pxx(2*length(pxx)-idx_f+1:length(pxx)))]);
            end
        end

        pxx_log_sm = 10*log10(pxx_sm);

        mask = ~isinf(pxx_log_sm) & ~isnan(pxx_log_sm);

        [xData, yData, w] = prepareCurveData( f_p(mask), pxx_sm(mask), 1./n_sm(mask)' );
   
        % Set up fittype and options.
        ft = fittype( 'a./x.^b+c', 'independent', 'x', 'dependent', 'y' );
        opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
        opts.Display = 'Off';
        opts.Lower = [1e-6,0,-Inf];
        opts.StartPoint = [0.02,1,1];
        opts.Upper = [1e6,2,Inf];
        opts.Weights = w;
%%
        plot(log10(xData),log10(yData),log10(xData),10*log(.01./xData.^.5+c))
%%
        % Fit model to data.
        [fitresult, gof] = fit( xData, yData, ft, opts );

        figure(1)
        plot(f_p,pxx_log,f_p,pxx_log_sm,'--k')
        xlim([0,1])
        xlabel('Frequency (Hz)')
        ylabel('PSD (dB-Arb)')

        figure(2)
        plot(f_p,pxx_log,f_p,pxx_log_sm,'--k')
        xlim([0,.025])
        xlabel('Frequency (Hz)')
        ylabel('PSD (dB-Arb)')

        figure(3)
        a = .02;
        b = 1;
        c = 1;
        plot(log10(f_p),pxx_log,'.',log10(f_p),pxx_log_sm,'--k',log10(f_p),10*log(fitresult(f_p)),'--r')
        xlim([log10(min(f_p(mask))),log10(max(f_p(mask)))])
        ylim([-40,80])
        xlabel('log10(f) (Hz)')
        ylabel('PSD (dB-Arb)')
        legend('Data','Smoothed',['Fit: $PSD = 20 \times \log_{10}(\frac{A}{f^{\alpha}+C}$: $\alpha = ' num2str(fitresult.b,'%1.2f') '$'],'Location','Northeast','Interpreter','latex')

%%
        if remoteSave
            if exist(['G:/My Drive/SrII/Misc/log_data/' name '/'],'dir')==0
                mkdir(['G:/My Drive/SrII/Misc/log_data/' name '/'])
            end
            copyfile([pathName '/data.mat'],['G:/My Drive/SrII/Misc/log_data/' name '/data.mat'])
            copyfile([pathName '/single_spectrum.png'],['G:/My Drive/SrII/Misc/log_data/' name '/single_spectrum.png'])
            copyfile([pathName '/full_log.png'],['G:/My Drive/SrII/Misc/log_data/' name '/full_log.png'])
            copyfile([pathName '/histogram.png'],['G:/My Drive/SrII/Misc/log_data/' name '/histogram.png'])
            copyfile([pathName '/peak_location.png'],['G:/My Drive/SrII/Misc/log_data/' name '/peak_location.png'])
            copyfile([pathName '/adev.png'],['G:/My Drive/SrII/Misc/log_data/' name '/adev.png'])
            copyfile([pathName '/peak_power.png'],['G:/My Drive/SrII/Misc/log_data/' name '/peak_power.png'])

        end
    end
% catch ex
%     clear rigol
%     save('AOM_drift_logging_backup.mat')
%     error(ex)
% end