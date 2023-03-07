#!/usr/bin/python
from subprocess import *
from sys import        *
import                 os
from timeit import     default_timer as timer

class WolframLink():
  """docstring for ClassName"""
  def __init__(self, rem = 1):
    self.wpath = "/home3/marcos.romero/Mathematica/"
    self.wtemp = self.wpath+"temp/temp.wls"
    self.rem = rem

  def WriteWolframScript(self, code, filename="untitled.wls"):
    with open(self.wtemp,"w") as wlfile:
      wlfile.write("#!/usr/local/bin/MathematicaScript -script" + "\n")
      wlfile.write('OutFile =   OpenWrite["' + self.wpath + 'temp/Output.txt", FormatType -> OutputForm];'+"\n")
      wlfile.write('$PrePrint = (Write[OutFile, #]; #) &;'+"\n")
      wlfile.write('PrintFile = OpenWrite["' + self.wpath + 'temp/Print.txt",  FormatType -> StandardForm];'+"\n")
      wlfile.write('AppendTo[$Output, PrintFile];'+"\n")
      wlfile.write('MessagesFile = OpenWrite["' + self.wpath + 'temp/Messages.txt", FormatType -> OutputForm];'+"\n")
      wlfile.write('AppendTo[$Messages, MessagesFile];')
      wlfile.write('SetOptions[First[$Output],FormatType->StandardForm];'+"\n")
      for line in code:
        wlfile.write(line+"\n")
      wlfile.write('Close[MessagesFile];$Messages=$Messages[[{1}]];'+"\n")
      wlfile.write('Close[PrintFile];$Output=$Output[[{1}]];'+"\n")
      wlfile.write('Close[OutFile];'+"\n")
    wlfile.close()
    os.chmod(self.wtemp, 0o777)

  def Run(self, filename="untitled.wls"):
    print "\n" + 80*"#" + "\n#" + 78*" " + "#"
    print "#" + 33*" " + "Wolfram link" + 33*" " + "#" + "\n#" + 78*" " + "#"
    print "Connection to nodo050.inv.usc.es opened."
    print "Temp file at: " + self.wtemp
    Time0 = timer()
    os.system('ssh -XYt nodo50 "'+ self.wtemp + '"')
    print "Evaluation Time: ", timer()-Time0, "s"
    print "#" + 78*" " + "#\n" + 80*"#" + "\n"
    if self.rem == 1:
      os.remove(self.wtemp)
    else:
      os.rename(self.wtemp,self.wpath+filename)

