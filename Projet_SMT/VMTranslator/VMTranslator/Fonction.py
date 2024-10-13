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
        return f"""\t//{self.command['type']} 

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
        Code assembleur de {self.command}\n

        """