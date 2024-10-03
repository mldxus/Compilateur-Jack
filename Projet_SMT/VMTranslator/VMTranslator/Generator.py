"""No comment"""

import sys
import Parser


class Generator:
    """
    La classe 'Generator' est responsable de la génération du code assembleur à partir
    des commandes VM analysées. Chaque type de commande est traduit en instructions
    spécifiques pour la machine Hack.
    """

    def __init__(self, file=None):
        """
        Initialise un objet 'Generator'. Si un fichier VM est fourni, il instancie un
        objet 'Parser' pour lire et analyser ce fichier.

        Args:
            file (str): Chemin vers un fichier VM à analyser.
        """
        if file is not None:
            self.parser = Parser.Parser(file)

    def __iter__(self):
        return self

    def __next__(self):
        if self.parser is not None and self.parser.hasNext():
            return self._next()
        else:
            raise StopIteration

    def _next(self):
        """
        Analyse la prochaine commande via le parser et appelle la méthode
        appropriée pour générer le code assembleur en fonction du type de commande.

        Returns:
            str: Code assembleur généré.
        """
        command = self.parser.next()
        if command is None:
            return None
        else:
            type = command['type']
            # type = push|pop|
            #        add|sub|neg|eq|gt|lt|and|or|not) |
            #        label|goto|if-goto|
            #        Function|Call|return

            match type:
                # Faire une fonction par type de commande
                case 'push':
                    return self._commandpush(command)
                case 'Call':
                    return self.commandcall(command)
                case 'pop' :
                    return self.commandpop(command)
                case 'add' :
                    return self.commandadd(command)
                case 'sub' :
                    return self.commandsub(command)
                case 'neg' :
                    return self.commandneg(command)
                case 'eq' :
                    return self.commandeq(command)
                case 'gt' :
                    return self.commandgt(command)
                case 'lt' :
                    return self.commandlt(command)
                case 'and' :
                    return self.commandand(command)
                case 'or' :
                    return self.commandor(command)
                case 'not' :
                    return self.commandnot(command)
                case _:
                    print(f'SyntaxError : {command}')
                    exit()

    def _commandpush(self, command):
         """
        Génère le code assembleur pour une commande 'push'.
        Appelle des méthodes spécifiques pour chaque type de segment.

        Args:
            command (dict): Commande VM avec ses arguments.

        Returns:
            str: Code assembleur généré pour la commande 'push'.
        """
        segment = command['segment']
        # segment=local|argument|static|constant|this|that|pointer
        match segment:
            # Faire une fonction par type de segment
            case 'constant':
                return self._commandpushconstant(command)
            case _:
                print(f'SyntaxError : {command}')
                exit()

    def _commandpushconstant(self, command):
        """
        Génère le code assembleur pour 'push constant i', qui place une constante 'i' sur la pile.

        Args:
            command (dict): Contient les informations de la commande (type, segment, valeur).

        Returns:
            str: Code assembleur pour `push constant i`.
        """
        parameter = command['parameter']
        return f"""\t//{command['type']} {command['segment']} {parameter}
    Code assembleur de {command}\n"""

    def _commandcall(self, command):
         """
        Génère le code assembleur pour une commande 'call' d'une fonction avec un certain nombre
        d'arguments.

        Args:
            command (dict): Contient les informations de la commande 'Call'.

        Returns:
            str: Code assembleur pour 'call function'.
        """
        return f"""\t//{command['type']} {command['function']} {command['parameter']}
    Code assembleur de {command}\n"""
    
    def commandadd(self,command) :
        return f"""\t//{command['type']} {command['function']} {command['parameter']}
    Code assembleur de {command}\n
    @SP
    M=M-1
    A=M
    D=M
    A=A-1
    M=D+M
    """
    
    def commandsub(self,command) :
        return f"""\t//{command['type']} {command['function']} {command['parameter']}
    Code assembleur de {command}\n
    @SP
    M=M-1
    A=M
    D=M
    A=A-1
    M=D-M
    """
    
    def commandneg(self,command) :
        return f"""\t//{command['type']} {command['function']} {command['parameter']}
    Code assembleur de {command}\n
    @SP
    M=M-1
    A=M
    D=M
    @0
    D=A-D
    @SP
    M=M-1
    A+M
    M+D
    """

    def commandeq(self,command) :
        return f"""\t//{command['type']} {command['function']} {command['parameter']}
    Code assembleur de {command}\n
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
    
    def commangt(self,command) :
        return f"""\t//{command['type']} {command['function']} {command['parameter']}
    Code assembleur de {command}\n
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
    
    def commanlt(self,command) :
        return f"""\t//{command['type']} {command['function']} {command['parameter']}
    Code assembleur de {command}\n
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
if __name__ == '__main__':
    file = sys.argv[1]
    print('-----debut')
    generator = Generator(file)
    for command in generator:
        print(command)
    print('-----fin')
