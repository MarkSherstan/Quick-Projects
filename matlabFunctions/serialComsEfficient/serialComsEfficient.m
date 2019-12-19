% Connect to serial port and set properties
s = serial('/dev/cu.usbmodem14101', 'BaudRate', 9600);
s.InputBufferSize = 20;
s.Timeout = 4;
fopen(s);

% Pause to begin a flow of data
pause(3);
fprintf("Connection established\n")

% Start a counter and timer
count = 0;
tic
startTimer = toc;

% Get data for 15 seconds
while (toc < startTimer+15)

  % Perform the header checks and cast bytes to ints
  if (fread(s, 1) == 159)
      if (fread(s, 1) == 110)
          x = fread(s, 2);
          analogOut = typecast(uint8(x), 'uint16');
      end
  end

  % Display data to the user
  fprintf("%d\n", analogOut)

  % Increment counter
  count = count + 1;
end

% Display sample rate to user
endTimer = toc;
fprintf("Sample rate was: %0.2f Hz\n", count/(endTimer - startTimer))

% Close serial port connection
fclose(s);
delete(s)
clear s
