import Parser
import sys

class BranchementCommand :
    def __init__(self, command):
        self.command = command

    def commandlabel(self):
        return f"""\t//{self.command['type']} 
        //Code assembleur de {self.command}\n
        ({self.command['label']})
        """

    def commandgoto(self):
        return f"""\t//{self.command['type']} 
        //Code assembleur de {self.command}\n
        @({self.command['label']})
        0;JMP
        """

    def commandifgoto(self):
        return f"""\t//{self.command['type']} 
        //Code assembleur de {self.command}\n
        @SP
        AM=M-1
        D=M+1
        @({self.command['label']})
        D;JEQ
        """