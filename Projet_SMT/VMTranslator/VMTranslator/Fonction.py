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
        Returns:
            str: Code assembleur généré pour l'appel de la fonction.
        """
        return_label = f"RETURN_LABEL_{self.return_label_count}"
        self.return_label_count += 1
        function_name = self.command['function']
        num_args = self.command['parameter']
        result = []
        
        # Sauvegarder l'adresse de retour
        result.append(f"@{return_label}")
        result.append("D=A")
        result.append("@SP")
        result.append("A=M")
        result.append("M=D")
        result.append("@SP")
        result.append("M=M+1")
        # Sauvegarder LCL, ARG, THIS, THAT
        for register in ["LCL", "ARG", "THIS", "THAT"]:
            result.append(f"@{register}")
            result.append("D=M")
            result.append("@SP")
            result.append("A=M")
            result.append("M=D")
            result.append("@SP")
            result.append("M=M+1")
        # ARG = SP - n - 5
        result.append("@SP")
        result.append("D=M")
        result.append(f"@{int(num_args) + 5}")
        result.append("D=D-A")
        result.append("@ARG")
        result.append("M=D")
        # LCL = SP
        result.append("@SP")
        result.append("D=M")
        result.append("@LCL")
        result.append("M=D")
        # Goto function
        result.append(f"@{function_name}")
        result.append("0;JMP")
        # Label de retour
        result.append(f"({return_label})")
        
        return "\n".join(result)