import Parser
import sys
from LabelGenerator import LabelGenerator

class PushCommand :
    def __init__(self, command):
        self.command = command
        self.label_generator = LabelGenerator()

    def executePush(self):
        segment = self.command['segment']
        match segment:
            case 'constant':
                return self._commandpushconstant()
            case 'local':
                return self._commandpushlocal()
            case 'argument':
                return self._commandpushargument()
            case 'static':
                return self._commandpushstatic()
            case 'this':
                return self._commandpushthis()
            case 'that':
                return self._commandpushthat()
            case 'temp':
                return self._commandpushtemp()
            case 'pointer':
                return self._commandpushpointer()
            case _:
                raise ValueError(f"SyntaxError : {segment}")

    def _commandpushconstant(self):
        parameter = self.command['parameter']
        return f"""
        // push constant {parameter}
        //Code assembleur de {self.command}\n
        @{parameter}
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """

    def _commandpushlocal(self):
        parameter = self.command['parameter']
        return f"""\t//{self.command['type']} {self.command['segment']} {parameter}
    //Code assembleur de {self.command}\n
    @LCL
    D=M
    @{parameter}
    A=D+A
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    """

    def _commandpushargument(self):
        parameter = self.command['parameter']
        return f"""\t//{self.command['type']} {self.command['segment']} {parameter}
    //Code assembleur de {self.command}\n
    @ARG
    D=M
    @{parameter}
    A=D+A
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    """

    def _commandpushthis(self):
        parameter = self.command['parameter']
        return f"""\t//{self.command['type']} {self.command['segment']} {parameter}
    //Code assembleur de {self.command}\n
    @THIS
    D=M
    @{parameter}
    A=D+A
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    """

    def _commandpushthat(self):
        parameter = self.command['parameter']
        return f"""\t//{self.command['type']} {self.command['segment']} {parameter}
    //Code assembleur de {self.command}\n
    @THAT
    D=M
    @{parameter}
    A=D+A
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    """

    def _commandpushstatic(self):
        parameter = self.command['parameter']
        return f"""\t//{self.command['type']} {self.command['segment']} {parameter}
    //Code assembleur de {self.command}\n
    @{parameter}
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    """

    def _commandpushtemp(self):
        parameter = self.command['parameter']
        return f"""\t//{self.command['type']} {self.command['segment']} {parameter}
    //Code assembleur de {self.command}\n
    @5
    D=A
    @{parameter}
    A=D+A
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    """

    def _commandpushpointer(self):
        parameter = self.command['parameter']
        IF_TRUE = self.label_generator.generate_label('IF_TRUE')
        END_IF = self.label_generator.generate_label('END_IF')
        return f"""\t//{self.command['type']} {self.command['segment']} {parameter}
    //Code assembleur de {self.command}\n
    @{parameter}
    D=A
    @{IF_TRUE}
    D;JEQ
    @THAT
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    @{END_IF}
    0;JMP
    ({IF_TRUE})
    @THIS
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    ({END_IF})
    """
