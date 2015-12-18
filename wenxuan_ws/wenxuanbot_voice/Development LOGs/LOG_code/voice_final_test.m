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
out_datas_3 = zeros(1,10000); 
out_times_3 = zeros(1,10000); 


tic;
try
    for i = 1:10000
        out_line = fscanf(s,'%f');
        out_datas_1(i) = out_line;
        out_times_1(i) = toc;
        out_line = fscanf(s,'%f');
        out_datas_2(i) = out_line;
        out_times_2(i) = toc;
        out_line = fscanf(s,'%f');
        out_datas_3(i) = out_line;
        out_times_3(i) = toc;        
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
subplot(3,1,1);
plot(out_times_1,out_datas_1);
axis([1,20,-600,600]);

subplot(3,1,2);
plot(out_times_2,out_datas_2);
axis([1,20,-600,600]);

subplot(3,1,3);
plot(out_times_2,out_datas_2);
axis([1,20,-600,600]);

sum(out_datas_1)
sum(out_datas_2)
sum(out_datas_3)
