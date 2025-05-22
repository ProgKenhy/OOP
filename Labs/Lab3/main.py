from myLogger import Logger, SimpleLogFilter, ConsoleHandler, FileHandler

myLogger = Logger(handlers=[ConsoleHandler(), FileHandler(filename='logfile.txt')], filters=[SimpleLogFilter(pattern="123")])

myLogger.write(message="13 121123 sda")
