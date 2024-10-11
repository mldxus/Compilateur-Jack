"""No comment"""

import sys
import Lexer

 
class Parser:
    """
    La classe 'Parser' est responsable d'analyser les commandes VM à partir du fichier
    et de les convertir en une représentation structurée qui peut être utilisée pour
    la génération de code assembleur.
    """

    def __init__(self, file):
        self.lexer = Lexer.Lexer(file)
        self.command = self._read()

    def next(self):
        """
        Retourne la commande actuelle et charge la suivante.

        Returns:
            dict: La commande actuelle avant de charger la suivante.
        """
        res = self.command
        self.command = self._read()
        return res

    def look(self):
        """
        Permet de consulter la commande actuelle sans avancer dans le fichier.

        Returns:
            dict: La commande actuelle.
        """
        return self.command

    def hasNext(self):
        """
        Vérifie s'il reste des commandes à analyser dans le fichier VM.

        Returns:
            bool: True s'il y a encore des commandes, False sinon.
        """
        return self.command is not None

    def __iter__(self):
        return self

    def __next__(self):
        if self.hasNext():
            return self.next()
        else:
            raise StopIteration

    def _read(self):
        """
        Lit et interprète la prochaine commande dans le fichier. Identifie le type de commande
        et appelle la méthode appropriée pour l'analyser.

        Returns:
            dict: La commande structurée avec ses arguments.
        """
        command = self.lexer.look()
        if command is None:
            return None
        else:
            type = command['type']
            match type:
                case 'pushpop':
                    return self._commandpushpop()
                case 'branching':
                    return self._commandbranching()
                case 'arithmetic':
                    return self._commandarithmetic()
                case 'function':
                    return self._commandfunction()
                case 'return':
                    return self._commandreturn()
                case 'call':
                    return self._commandcall()
                case _:
                    print(f'SyntaxError : {command}')
                    exit()

    def _commandarithmetic(self):
        """
        Traite les commandes arithmétiques comme `add`, `sub`, `neg`.

        Returns:
            dict: Commande avec type et informations associées.
        """
        command = self.lexer.next()
        return {'line': command['line'], 'col': command['col'], 'type': command['token']}

    def _commandpushpop(self):
        """
        Traite les commandes `push` et `pop`, en vérifiant le segment et le paramètre associés.

        Returns:
            dict: Commande structurée avec type, segment et paramètre.
        """
        command = self.lexer.next()
        segment = self.lexer.next()
        parameter = self.lexer.next()
        if segment is None or parameter is None or segment['type'] != 'segment' or parameter['type'] != 'int':
            print(f"SyntaxError (line={command['line']}, col={command['col']}): {command['token']}")
            exit()

        return {'line': command['line'], 'col': command['col'], 'type': command['token']
            , 'segment': segment['token'], 'parameter': parameter['token']}

    def _commandbranching(self):
        command = self.lexer.next()
        label = self.lexer.next()
        if label is None or label['type'] != 'string':
            print(f"SyntaxError (line={command['line']}, col={command['col']}): {command['token']}")
            exit()

        return {'line': command['line'], 'col': command['col'], 'type': command['token']
            , 'label': label['token']}

    def _commandfunction(self):
        command = self.lexer.next()
        name = self.lexer.next()
        parameter = self.lexer.next()
        if name is None or parameter is None or name['type'] != 'string' or parameter['type'] != 'int':
            print(f"SyntaxError (line={command['line']}, col={command['col']}): {command['token']}")
            exit()

        return {'line': command['line'], 'col': command['col'], 'type': command['token']
            , 'function': name['token'], 'parameter': parameter['token']}

    def _commandreturn(self):
        command = self.lexer.next()
        return {'line': command['line'], 'col': command['col'], 'type': command['token']}
    
    def _commandcall(self):
        command = self.lexer.next()
        function_name = self.lexer.next()
        num_args = self.lexer.next()
        if function_name is None or num_args is None or function_name['type'] != 'string' or num_args['type'] != 'int':
            print(f"SyntaxError (line={command['line']}, col={command['col']}): {command['token']}")
            exit()

        return {'line': command['line'], 'col': command['col'], 'type': 'call', 'function': function_name['token'], 'parameter': num_args['token']}

    


if __name__ == "__main__":
    file = sys.argv[1]
    print('-----debut')
    parser = Parser(file)
    for command in parser:
        print(command)
    print('-----fin')
