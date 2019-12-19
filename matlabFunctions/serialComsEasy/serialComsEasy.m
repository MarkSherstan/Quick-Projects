% Connect to serial port
s = serial('/dev/cu.usbmodem14101', 'BaudRate', 115200);
fopen(s);
pause(3);
fprintf("Connection established\n")

% Start a counter and timer
count = 0;
tic
startTimer = toc;

% Get data for 15 seconds
while (toc < startTimer+15)
  % Send character and receive data (handshake protocal)
  fprintf(s, "a");
  out = fscanf(s, '%d\n');

  % Display data to user
  fprintf("%d\n",out)

  % Increment counter
  count = count + 1;
end

% Display sample rate to user
endTimer = toc;
fprintf("Sample rate was: %0.2f Hz\n",count/(endTimer - startTimer))

% Remove/close serial port connection
fclose(s);
delete(s)
clear s
