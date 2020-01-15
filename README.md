psst stuffs been resolved. wb BM



# Advice from Ana M.

  Read the NWR Specifications document BEFORE you 
  use this program. It will answer 90% of all 
  questions you will have. All NWR documents can
  be found on weather.gov, or click [https://www.nws.noaa.gov/directives/sym/pd01017012curr.pdf](HERE) for the
  specific NWR SAME Directives PDF.
  
  Thank you!

# Quick Message from Authors:

  Hi! Just here to tell you that we are NOT responsible for 
    any improper EAS activations that occur because of use of
    this program. If for some reason that equiptment is 
    activated, the person responsible for activating such 
    is whom transmitted it. We have disabled some event codes
    just in case. but Please, for the love of everything holy, 
    be responsible. Responsible people take the blame for what
    they have done. DO NOT send these tones over the airwaves.
    No matter what, you will be accountable for missuse of the
    tones. 

    AGAIN: YOU ARE RESPONSIBLE FOR YOUR SHENANIGANS! We aren't!



         Thank you for reading this, and by using this 
      program you agree to such terms above.


In other words, use at your own risk. This software is for testing
purposes only. No guarantees of suitability or compatibility
with any FCC approved EAS decoders are expressed or implied. 
Users of the software are encouraged to do extensive testing
before using in a production environment, if ever.

# HOW TO USE:

You will need Python 2.7 (we reccomend Python 2.7.17!)


Most of you use windows, so we have made a batch file for 
you to run! As long as you have everything downloaded in the
same directory and python installed, you should be able to 
launch the program with no trouble! 






The executable file is a compiled version of the four
Python scripts easencode.py (the commandline interface),
eastestgen.py (EAS message formatting), afsk.py (afsk routines),
and audioroutines.py (library functions for signal generation).
The scripts were developed using Python 2.7 and should run
correctly in any platform where Python 2.7 is installed.

The executable file easencode.exe (easencode.py) provides 
a simple commandline implementation of an EAS encoder. You 
pass it the configuration details and the result is a WAVE
file that *should* be an EAS message according to the 
structure defined by the FCC rules. This flexibility allows
the user the ability to generate a variety of activation
messages and observe the way the decoder reacts. Consult 
the FCC rules for the correct values for FIPS codes and
activation messages.

Some basic help is available on the commandline using the 
(-h) help option.

# USAGE EXAMPLES (For Command-Line Use) 
# ***NOT RECOMMENDED!!! USE THE BATCH FILE!!!***

Generate a simple test
    easencode.py -o EAS -e RWT -f 029177 -t now -c "WXYZ/FM" eas-rwt.wav
    easencode.py -o EAS -e RWT -f 029177 -t now -c "WXYZ/FM" eas-rwt.wav

Generate a test with a voice message from input.wav
    easencode.py -o EAS -e RWT -f 037124 -c "KXYZ/FM" -a input.wav eas-rwt.wav
    
Generate EOMs
    easencode.py -o EAS -e RWT -f 005007 -t now -c "KXYZ/FM -x yes eas-rwt-eom.wav
    
    
# License (see the MIT License)
 Copyright (c) 2019 EAS Alert Team

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
