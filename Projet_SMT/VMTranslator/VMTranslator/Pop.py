import Parser
import sys

class PopCommand :
    def __init__(self, command):
        self.command = command

    def executePop(self):
        """ Génère le code assembleur pour une commande 'pop'.
            Appelle des méthodes spécifiques pour chaque type de segment.

            Args:
                command (dict): Commande VM avec ses arguments.

            Returns:
                str: Code assembleur généré pour la commande 'pop'.
         """
        segment = self.command['segment']
        # segment=local|argument|static|this|that|pointer
        match segment:
                # Faire une fonction par type de segment
                case 'local':
                    return self._commandpoplocal()
                case 'argument':
                    return self._commandpopargument()
                case 'static':
                    return self._commandpopstatic()
                case 'this':
                    return self._commandpopthis()
                case 'that':
                    return self._commandpopthat()
                case 'pointer':
                    return self._commandpoppointer()
                case 'temp':
                    return self._commandpoptemp()
                case _:
                    raise ValueError(f"SyntaxError : {segment}")

    def _commandpoplocal(self):
        parameter = self.command['parameter']
        return f"""\t//{self.command['type']} {self.command['segment']} {parameter}
    Code assembleur de {self.command}\n
    @LCL
    D=M
    @{parameter}
    D=D+A
    @R13
    M=D
    @SP
    AM=M-1
    D=M
    @R13
    A=M
    M=D
    """

    def _commandpopargument(self):
        parameter = self.command['parameter']
        return f"""\t//{self.command['type']} {self.command['segment']} {parameter}
    Code assembleur de {self.command}\n
    @ARG
    D=M
    @{parameter}
    D=D+A
    @R13
    M=D
    @SP
    AM=M-1
    D=M
    @R13
    A=M
    M=D
    """

    def _commandpopthis(self):
        parameter = self.command['parameter']
        return f"""\t//{self.command['type']} {self.command['segment']} {parameter}
    Code assembleur de {self.command}\n
    @THIS
    D=M
    @{parameter}
    D=D+A
    @R13
    M=D
    @SP
    AM=M-1
    D=M
    @R13
    A=M
    M=D
    """

    def _commandpopthat(self):
        parameter = self.command['parameter']
        return f"""\t//{self.command['type']} {self.command['segment']} {parameter}
    Code assembleur de {self.command}\n
    @THAT
    D=M
    @{parameter}
    D=D+A
    @R13
    M=D
    @SP
    AM=M-1
    D=M
    @R13
    A=M
    M=D
    """

    def _commandpopstatic(self):
        parameter = self.command['parameter']
        return f"""\t//{self.command['type']} {self.command['segment']} {parameter}
    Code assembleur de {self.command}\n
    @SP
    AM=M-1
    D=M
    @{parameter}
    M=D
    """

    def _commandpoptemp(self):
        parameter = self.command['parameter']
        return f"""\t//{self.command['type']} {self.command['segment']} {parameter}
    Code assembleur de {self.command}\n
    @5
    D=A
    @{parameter}
    D=D+A
    @R13
    M=D
    @SP
    AM=M-1
    D=M
    @R13
    A=M
    M=D
    """

    def _commandpoppointer(self):
        parameter = self.command['parameter']
        return f"""\t//{self.command['type']} {self.command['segment']} {parameter}
    Code assembleur de {self.command}\n
    @{parameter}
    D=A
    @IF_TRUE
    D;JEQ
    @SP
    AM=M-1
    D=M
    @THAT
    M=D
    @END_IF
    0;JMP
    (IF_TRUE)
    @SP
    AM=M-1
    D=M
    @THIS
    M=D
    (END_IF)
    """