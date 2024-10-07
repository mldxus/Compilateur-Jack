"""Affiche '-----debut'
Affiche le tableau crée par la class Reader
Affiche '-----fin'
""" 

import os
import sys


class Reader:
    """
    La classe 'Reader' est responsable de la lecture caractère par caractère du fichier VM.
    Elle garde une trace des lignes et colonnes pour permettre une bonne gestion des erreurs.
    """

    def __init__(self, file):
        self.char = None
        self._line = 1
        self._col = 1
        if os.path.exists(file):
            self.file = open(file, "r")
            self.char = self.file.read(1)

    def look(self):
        """
        Retourne le caractère actuel avec sa position (ligne, colonne).

        Returns:
            dict: Le caractère actuel avec sa ligne et sa colonne.
        """
        return {'line': self._line, 'col': self._col, 'char': self.char}

    def next(self):
        """
        Avance au caractère suivant, en ajustant la ligne et la colonne en fonction
        du caractère lu (nouvelle ligne ou caractère simple).

        Returns:
            dict: Le caractère précédent avec sa ligne et sa colonne.
        """
        res = {'line': self._line, 'col': self._col, 'char': self.char}
        if self.hasNext():
            if self.char == '\n':
                self._line += 1
                self._col = 1
            else:
                self._col += 1
            self.char = self.file.read(1)
            if not self.hasNext():
                self.file.close()
        return res

    def hasNext(self):
        """
        Vérifie s'il reste des caractères à lire dans le fichier.

        Returns:
            bool: True s'il reste des caractères, False sinon.
        """
        if self.char:
            return True
        else:
            return False

    def __iter__(self):
        return self

    def __next__(self):
        if self.hasNext():
            return self.next()
        else:
            raise StopIteration


if __name__ == "__main__":
    file = sys.argv[1]
    print('-----debut')
    lecteur = Reader(file)
    for c in lecteur:
        print(c)
    print('-----fin')
