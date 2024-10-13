"""No comment"""

import sys
import Parser
from Push import PushCommand
from Pop import PopCommand
from Arithmetiques import AriCommand
from Logique import LogiqueCommand
from Branchement import BranchementCommand
from Fonction import FonctionCommand

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
                    push_command = PushCommand(command)
                    return push_command.executePush()
                case 'Call':
                    call_command = FonctionCommand(command)
                    return call_command._commandcall()
                case 'pop' :
                    pop_command = PopCommand(command)
                    return pop_command.executePop()
                case 'add' :
                    add_command = AriCommand(command)
                    return add_command.commandadd()
                case 'sub' :
                    sub_command = AriCommand(command)
                    return sub_command.commandsub()
                case 'neg' :
                    neg_command = AriCommand(command)
                    return neg_command.commandneg()
                case 'eq' :
                    eq_command = LogiqueCommand(command)
                    return eq_command.commandeq()
                case 'gt' :
                    gt_command = LogiqueCommand(command)
                    return gt_command.commandgt()
                case 'lt' :
                    lt_command = LogiqueCommand(command)
                    return lt_command.commandlt()
                case 'and' :
                    and_command = LogiqueCommand(command)
                    return and_command.commandand()
                case 'or' :
                    or_command = LogiqueCommand(command)
                    return or_command.commandor()
                case 'not' :
                    not_command = LogiqueCommand(command)
                    return not_command.commandnot()
                case 'label' :
                    label_command = BranchementCommand(command)
                    return label_command.commandlabel()
                case 'goto':
                    goto_command = BranchementCommand(command)
                    return goto_command.commandgoto()
                case 'if-goto':
                    ifgoto_command = BranchementCommand(command)
                    return ifgoto_command.commandifgoto()
                case 'Function' :
                    Function_command = FonctionCommand(command)
                    return Function_command.commandfunction()
                case 'return' :
                    return_command = FonctionCommand(command)
                    return return_command.commandreturn()
                case _:
                    print(f'SyntaxError : {command}')
                    exit()


if __name__ == '__main__':
    file = sys.argv[1]
    print('-----debut')
    generator = Generator(file)
    for command in generator:
        print(command)
    print('-----fin')
