"""Wexpect is a Windows variant of pexpect https://pexpect.readthedocs.io.

Wexpect is a Python module for spawning child applications and controlling
them automatically. 

wexpect util contains small functions, and classes, which are used in multiple classes.
The command line argument parsers, and the Exceptions placed here.

Credits: Noah Spurrier, Richard Holden, Marco Molteni, Kimberley Burchett,
Robert Stone, Hartmut Goebel, Chad Schroeder, Erick Tryzelaar, Dave Kirby, Ids
vander Molen, George Todd, Noel Taylor, Nicolas D. Cesar, Alexander Gattin,
Geoffrey Marshall, Francisco Lourenco, Glen Mabey, Karthik Gurusamy, Fernando
Perez, Corey Minyard, Jon Cohen, Guillaume Chazarain, Andrew Ryan, Nick
Craig-Wood, Andrew Stone, Jorgen Grahn, Benedek Racz

Free, open source, and all that good stuff.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Wexpect Copyright (c) 2019 Benedek Racz

"""

import re
import ctypes
import traceback
import sys

def split_command_line(command_line):
    '''https://stackoverflow.com/a/35900070/2506522
    '''
    
    nargs = ctypes.c_int()
    ctypes.windll.shell32.CommandLineToArgvW.restype = ctypes.POINTER(ctypes.c_wchar_p)
    lpargs = ctypes.windll.shell32.CommandLineToArgvW(command_line, ctypes.byref(nargs))
    args = [lpargs[i] for i in range(nargs.value)]
    if ctypes.windll.kernel32.LocalFree(lpargs):
        raise AssertionError
    return args

def join_args(args):
    """Joins arguments into a command line. It quotes all arguments that contain
    spaces or any of the characters ^!$%&()[]{}=;'+,`~"""
    commandline = []
    for arg in args:
        if re.search('[\^!$%&()[\]{}=;\'+,`~\s]', arg):
            arg = '"%s"' % arg
        commandline.append(arg)
    return ' '.join(commandline)


class ExceptionPexpect(Exception):
    """Base class for all exceptions raised by this module.
    """

    def __init__(self, value):

        self.value = value

    def __str__(self):

        return str(self.value)

    def get_trace(self):
        """This returns an abbreviated stack trace with lines that only concern
        the caller. In other words, the stack trace inside the Wexpect module
        is not included. """

        tblist = traceback.extract_tb(sys.exc_info()[2])
        tblist = [item for item in tblist if self.__filter_not_wexpect(item)]
        tblist = traceback.format_list(tblist)
        return ''.join(tblist)

    def __filter_not_wexpect(self, trace_list_item):
        """This returns True if list item 0 the string 'wexpect.py' in it. """

        if trace_list_item[0].find('wexpect.py') == -1:
            return True
        else:
            return False


class EOF(ExceptionPexpect):
    """Raised when EOF is read from a child. This usually means the child has exited.
    The user can wait to EOF, which means he waits the end of the execution of the child process."""

class TIMEOUT(ExceptionPexpect):
    """Raised when a read time exceeds the timeout. """

