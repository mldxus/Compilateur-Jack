import Parser
import sys

class FonctionCommand :
    def __init__(self, command):
        self.command = command

    def commandfunction(self):
        TRUC = """@SP
        A=M
        M=0
        @SP
        M=M+1
        """
        return f"""\t//{self.command['type']} 
        //
        ({self.command['function']})

        """ + int(self.command['parameter']) * TRUC

    def commandreturn(self):
        """
        Génère le code assembleur pour une commande 'return'. Cela retourne d'une fonction en
        restaurant l'état de l'appelant.

        Returns:
            str: Code assembleur généré pour la commande 'return'.
        """
        return f"""\t// return

        // Sauvegarder FRAME = LCL
        @LCL
        D=M
        @R13
        M=D

        // RET = *(FRAME - 5)
        @5
        A=D-A
        D=M
        @R14
        M=D

        // *ARG = pop()
        @SP
        AM=M-1
        D=M
        @ARG
        A=M
        M=D

        // SP = ARG + 1
        @ARG
        D=M+1
        @SP
        M=D

        // Restaurer THAT, THIS, ARG, LCL
        @R13
        AM=M-1
        D=M
        @THAT
        M=D
        @R13
        AM=M-1
        D=M
        @THIS
        M=D
        @R13
        AM=M-1
        D=M
        @ARG
        M=D
        @R13
        AM=M-1
        D=M
        @LCL
        M=D

        // Retour à l'appelant (GOTO RET)
        @R14
        A=M
        0;JMP
        """


    def _commandcall(self):
        """
       Génère le code assembleur pour une commande 'call' d'une fonction avec un certain nombre
       d'arguments.

       Args:
           command (dict): Contient les informations de la commande 'Call'.

       Returns:
           str: Code assembleur pour 'call function'.
       """
        parameter = self.command['parameter']
        return f"""\t//{self.command['type']} {self.command['function']} {self.command['parameter']}
        //Code assembleur de {self.command}\n

        """