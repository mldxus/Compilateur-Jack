import Parser
import sys

class AriCommand :
    def __init__(self, command):
        self.command = command

    def commandadd(self):
        return f"""\t//{self.command['type']}  
    //Code assembleur de {self.command}\n
    @SP
    AM=M-1
    D=M
    A=A-1
    M=D+M
    """

    def commandsub(self):
        return f"""\t//{self.command['type']} 
    //Code assembleur de {self.command}\n
    @SP
    M=M-1
    A=M
    D=M
    A=A-1
    M=M-D
    """

    def commandneg(self):
        return f"""\t//{self.command['type']} 
    //Code assembleur de {self.command}\n
    @SP
    A=M-1
    M=-M
    """