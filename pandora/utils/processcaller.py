"""Caller class for subprocess"""
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
#import signal
from pandora.config import DEBUG
from pandora.utils.utils import bytes_to_string
import os
DEVNULL = open(os.devnull, "wb")

class ProcessCaller():
    def __init__(self):
        self.proc = None

    def runwait(self, cmd, timeout=None):
        self._execute(cmd)
        return self._wait(timeout=timeout)

    def runread(self, cmd, timeout=None):
        self._execute(cmd)
        return self._communicate(timeout=timeout)

    def executeret(self, cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT):
        if DEBUG:
            print(f"Executing: {cmd}")
        return Popen(cmd, stdin=stdin, stdout=stdout, stderr=stderr)

    def executeretnull(self, cmd):
        if DEBUG:
            print(f"Executing: {cmd}")
        return Popen(cmd, stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)

    def _execute(self, cmd):
        if DEBUG:
            print(f"Executing: {cmd}")
        self.proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)

    def _wait(self, timeout=None):
        if timeout and timeout > 1:
            try:
                self.proc.wait(timeout=timeout-1)
                success = True
            except TimeoutExpired:
                success = False
                try:
                    #self.proc.send_signal(signal.SIGINT)
                    self.proc.terminate()
                    self.proc.wait(timeout=1)
                except TimeoutExpired:
                    self.proc.kill()
                    self.proc.wait()
                    print(f"WARNING: Process {self.proc.pid} killed")
        else:
            self.proc.wait()
            success = True
        return success

    def _communicate(self, timeout=None):
        out, err = None, None
        stdout, stderr = None, None
        if timeout and timeout > 1:
            try:
                stdout, stderr = self.proc.communicate(timeout=timeout-1)
            except TimeoutExpired:
                try:
                    #self.proc.send_signal(signal.SIGINT)
                    self.proc.terminate()
                    stdout, stderr = self.proc.communicate(timeout=1)
                except TimeoutExpired:
                    self.proc.kill()
                    self.proc.wait()
                    stdout, stderr = self.proc.communicate()
                    print(f"WARNING: Process {self.proc.pid} killed")
        else:
            stdout, stderr = self.proc.communicate()
        out = bytes_to_string(stdout)
        err = bytes_to_string(stderr)
        return out, err
