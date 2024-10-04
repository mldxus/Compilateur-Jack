"""No comment"""
import os
import glob
import sys

import Generator


class Translator:
    """
    La classe 'Translator' est responsable de la traduction des fichiers VM (ou d'un dossier contenant plusieurs fichiers VM)
    en code assembleur pour la machine Hack. Elle utilise la classe 'Generator' pour générer le code assembleur
    correspondant à chaque commande VM, après avoir interprété le fichier.
    """

def __init__(self, files, asm):
        self.asm = open(asm, "w")
        self.files = files

def translate(self):
        """
        Cette méthode principale traduit un ou plusieurs fichiers VM en code assembleur Hack.
        Elle écrit d'abord le code de démarrage (bootstrap), puis traduit chaque fichier '.vm'.
        Si 'files' est un fichier unique, il est traduit. Si c'est un dossier, tous les fichiers '.vm' sont traduits.
        """
        self.asm.write(self._bootstrap())
        # os.listdir("/home/olivier")
        if os.path.isfile(self.files):
            self._translateonefile(self.files)
        else:
            if os.path.isdir(self.files):
                for file in glob.glob(f'{self.files}/*.vm'):
                    self._translateonefile(file)

def _translateonefile(self, file):
        """
        Cette méthode traduit un seul fichier '.vm' en code assembleur.
        Chaque commande VM du fichier est traduite en code assembleur à l'aide de la classe 'Generator'.

        Args:
            file (str): Le chemin du fichier VM à traduire.
        """
        self.asm.write(f"""\n//code de {file}\n""")
        generator = Generator.Generator(file)
        for command in generator:
            self.asm.write(command)

        def _bootstrap(self):
            """
        Génère le code assembleur nécessaire pour initialiser la pile à l'adresse 256 et appeler la fonction 'Sys.init'.
        Ce code est requis pour que la machine virtuelle Hack puisse démarrer correctement.

        Returns:
            str: Le code assembleur de démarrage (bootstrap).
        """
        init = Generator.Generator()._commandcall({'type': 'Call', 'function': 'Sys.init', 'parameter': '0'})

        return f"""// Bootstrap
    @256
    D=A
    @SP
    M=D
{init}
"""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: Translotor.py <vm file| dir> <asm file>")
    else:
        vmfiles=sys.argv[1]
        asmfile=sys.argv[2]
        translator = Translator(vmfiles,asmfile)
        translator.translate()