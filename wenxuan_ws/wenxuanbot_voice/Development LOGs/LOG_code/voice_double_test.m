%% clean up
clear all;
newobjs = instrfind;
if ~isempty(newobjs)
    fclose(newobjs);
    delete(newobjs);
end
%% start up
s = serial('/dev/tty.usbmodem1451');
set(s,'BaudRate',230400);
fopen(s);
pause(5);

%% read data
out_datas_1 = zeros(1,10000); 
out_times_1 = zeros(1,10000); 
out_datas_2 = zeros(1,10000); 
out_times_2 = zeros(1,10000); 


tic;
try
    for i = 1:10000
        out_line = fscanf(s,'%f');
        out_datas_1(i) = out_line;
        out_times_1(i) = toc;
        out_line = fscanf(s,'%f');
        out_datas_2(i) = out_line;
        out_times_2(i) = toc;
        
    end
catch exception
    warning('read failed');
    msgString = getReport(exception);
    warning(msgString);
end
%% cleanup
fclose(s);
delete(s);

%% plotting
figure(1);
subplot(2,1,1);
plot(out_times_1,out_datas_1);
axis([1,10,-500,1000]);

subplot(2,1,2);
plot(out_times_2,out_datas_2);
axis([1,10,-500,1000]);

(sum(out_datas_1) - sum(out_datas_2))/sum(out_datas_2)
