import Parser
import sys

class LogiqueCommand :
    def __init__(self, command):
        self.command = command

    def commandeq(self):
        return f"""\t//{self.command['type']} 
    //Code assembleur de {self.command}\n
    @SP
    M=M-1
    A=M
    D=M
    A=A-1
    D=D-M
    @IF_TRUE
    D;JEQ
    @SP
    A=M
    M=0
    @END_IF
    0,JMP
    (IF_TRUE)
    @0
    D=A
    @SP
    A=M-1
    M=D-1
    (END_IF)
    """

    def commandgt(self):
        return f"""\t//{self.command['type']} 
    //Code assembleur de {self.command}\n
    @SP
    M=M-1
    A=M
    D=M
    A=A-1
    D=D-M
    @IF_TRUE
    D;JGT
    @SP
    A=M
    M=0
    @END_IF
    0,JMP
    (IF_TRUE)
    @0
    D=A
    @SP
    A=M-1
    M=D-1
    (END_IF)
    """

    def commandlt(self):
        return f"""\t//{self.command['type']} 
    //Code assembleur de {self.command}\n
    @SP
    M=M-1
    A=M
    D=M
    A=A-1
    D=D-M
    @IF_TRUE
    D;JLT
    @SP
    A=M
    M=0
    @END_IF
    0,JMP
    (IF_TRUE)
    @0
    D=A
    @SP
    A=M-1
    M=D-1
    (END_IF)
    """

    def commandand(self):
        return f"""\t//{self.command['type']} 
    //Code assembleur de {self.command}\n
    @SP
    AM=M-1
    D=M
    @SP
    AM=M-1
    M=D&M
    @SP
    M=M+1
    """

    def commandor(self):
        return f"""\t//{self.command['type']} 
    //Code assembleur de {self.command}\n
    @SP
    AM=M-1
    D=M
    @SP
    AM=M-1
    M=D|M
    @SP
    M=M+1
    """

    def commandnot(self):
        return f"""\t//{self.command['type']} 
        //Code assembleur de {self.command}\n
        @SP
        A=M-1
        M=!M
        """