"""No comment"""
import sys
import Parser


class Generator:
    """No comment"""

    def __init__(self, file=None):
        if file is not None:
            self.parser = Parser.Parser(file)
            self.arbre = self.parser.jackclass()
            self.vmfile = open(self.arbre['name'] + '.vm', "w")
            self.symbolClassTable = []
            self.symbolRoutineTable = []

    def jackclass(self, arbre):
        """
            {'line': line, 'col': col, 'type': 'class', 'name': className,
            'varDec': [variable], 'subroutine':[subroutine]}
        """
        # Initialisation des tables de symboles pour la classe
        self.symbolClassTable = []
        self.symbolRoutineTable = []
        
        # Parcours des déclarations de variables
        for var in arbre['classVarDecs']:
            self.variable(var)
        
        # Parcours des sous-programmes
        for subroutine in arbre['subroutines']:
            self.subroutineDec(subroutine)
        
    def variable(self, var):
        """
        {'line': line, 'col': col, 'name': varName, 'kind': kind, 'type': type}
        """
        self.symbolClassTable.append({
            'name': var['name'],
            'type': var['type'],
            'kind': var['kind']
        })
        
    def subroutineDec(self, routine):
        """
        {'line':line, 'col': col,'type': 'constructor'|'function'|'method',
            'return' : 'void| 'int'|'char'|'boolean'|className',
            'name': subroutineName, 'argument': [variable],'local': [variable],
            'instructions' : [instruction]
        """
        # Réinitialisation de la table des symboles de sous-routine
        self.symbolRoutineTable = []

        # Ajoute les arguments à la table des symboles
        for arg in routine['argument']:
            self.variable(arg)
        
        # Ajoute les variables locales à la table des symboles
        for local in routine['local']:
            self.variable(local)
        
        # Génère l'en-tête VM
        self.vmfile.write(f"function {self.arbre['name']}.{routine['name']} {len(routine['local'])}\n")
        
        # Gestion spéciale pour les méthodes et constructeurs
        if routine['type'] == 'constructor':
            self.vmfile.write("push constant X\n")  # Allouer mémoire (exemple)
            self.vmfile.write("call Memory.alloc 1\n")
            self.vmfile.write("pop pointer 0\n")  # THIS pointe vers l'objet
        elif routine['type'] == 'method':
            self.vmfile.write("push argument 0\n")
            self.vmfile.write("pop pointer 0\n")  # THIS pointe vers l'objet courant
        
        # Génère le code pour le corps de la sous-routine
        for inst in routine['instructions']:
            self.statement(inst)

    def statement(self, inst):
        """
        statement : letStatements|ifStatement|whileStatement|doStatement|returnStatement
        """
        if inst['type'] == 'let':
            self.letStatement(inst)
        elif inst['type'] == 'if':
            self.ifStatement(inst)
        elif inst['type'] == 'while':
            self.whileStatement(inst)
        elif inst['type'] == 'do':
            self.doStatement(inst)
        elif inst['type'] == 'return':
            self.returnStatement(inst)
            
    def letStatement(self, inst):
        """
        {'line':line, 'col': col,'type': 'let',
        'variable': varName, 'indice': expression, 'valeur': expression
        """
        self.expression(inst['value'])
        self.vmfile.write(f"pop {self.getSegment(inst['variable'])} {self.getIndex(inst['variable'])}\n")

    def ifStatement(self, inst):
        """
        {'line':line, 'col': col,
        'type': 'if', 'condition': expression, 'true': [instruction],
        'false': [instruction]}
        """
        labelTrue = f"LABEL_TRUE_{self.label_count}"
        labelEnd = f"LABEL_END_{self.label_count}"
        self.label_count += 1
        
        # Évaluation de la condition
        self.expression(inst['condition'])
        self.vmfile.write(f"if-goto {labelTrue}\n")  # Si condition vraie, saut vers labelTrue
        # Sinon, sauter directement à la fin
        self.vmfile.write(f"goto {labelEnd}\n")
        self.vmfile.write(f"label {labelTrue}\n")
        
        # Génération du bloc 'true'
        for statement in inst['true']:
            self.statement(statement)
        
        self.vmfile.write(f"label {labelEnd}\n")
    
    def whileStatement(self, inst):
        """
        {'line':line, 'col': col,
        'type': 'while', 'condition': expression,
        'instructions': [instruction]}
        """
        labelStart = f"LABEL_WHILE_START_{self.label_count}"
        labelEnd = f"LABEL_WHILE_END_{self.label_count}"
        self.label_count += 1
        
        # Début de la boucle
        self.vmfile.write(f"label {labelStart}\n")
        
        # Évaluation de la condition
        self.expression(inst['condition'])
        self.vmfile.write(f"if-goto {labelEnd}\n")  # Sortir de la boucle si condition fausse
        
        # Corps de la boucle
        for statement in inst['instructions']:
            self.statement(statement)
        
        # Retour au début de la boucle
        self.vmfile.write(f"goto {labelStart}\n")
        self.vmfile.write(f"label {labelEnd}\n")
    
    def doStatement(self, inst):
        """
        {'line':line, 'col': col,
        'type': 'do', 'classvar': className ou varName,
        'name': subroutineName, 'argument': [expression]}
        """
        # Appel de la sous-routine
        self.subroutineCall(inst)
        # Supprime la valeur de retour (les appels `do` n'utilisent pas la valeur)
        self.vmfile.write("pop temp 0\n")
        
    def returnStatement(self, inst):
        """
        {'line':line, 'col': col, 'type': 'return', 'valeur': expression}
        """
        if inst['valeur']:
        # Retourne une valeur
            self.expression(inst['valeur'])
        else:
        # Retourne 0 par défaut (pour les fonctions void)
            self.vmfile.write("push constant 0\n")
        self.vmfile.write("return\n")

    def expression(self, exp):
        """
        [term op ...]
            avec op : '+'|'-'|'*'|'/'|'&'|'|'|'<'|'>'|'='
        """
        # Premier terme
        self.term(exp[0])
        
        # Parcours des opérations et termes suivants
        for i in range(1, len(exp), 2):
            op = exp[i]['value']
            self.term(exp[i + 1])
            
            # Correspondance des opérateurs
            if op == '+':
                self.vmfile.write("add\n")
            elif op == '-':
                self.vmfile.write("sub\n")
            elif op == '*':
                self.vmfile.write("call Math.multiply 2\n")
            elif op == '/':
                self.vmfile.write("call Math.divide 2\n")
            elif op == '&':
                self.vmfile.write("and\n")
            elif op == '|':
                self.vmfile.write("or\n")
            elif op == '<':
                self.vmfile.write("lt\n")
            elif op == '>':
                self.vmfile.write("gt\n")
            elif op == '=':
                self.vmfile.write("eq\n")
            
    def term(self, t):
        """
        {'line':line, 'col': col,
        'type': 'int'| 'string'| 'constant'| 'varName'|'call'| 'expression'|'-'|'~',
         'indice':expression, 'subroutineCall': subroutineCall}
        """
        if t['type'] == 'integerConstant':
            self.vmfile.write(f"push constant {t['value']}\n")
        elif t['type'] == 'stringConstant':
            self.writeStringConstant(t['value'])
        elif t['type'] == 'varName':
            self.vmfile.write(f"push {self.getSegment(t['name'])} {self.getIndex(t['name'])}\n")
        elif t['type'] == 'expression':
            self.expression(t['value'])
        elif t['type'] == 'unaryOp':
            self.term(t['term'])
            if t['op'] == '-':
                self.vmfile.write("neg\n")
            elif t['op'] == '~':
                self.vmfile.write("not\n")
                
    def subroutineCall(self, call):
        """
        {'line':line, 'col': col, 'classvar': className ou varName,
        'name': subroutineName, 'argument': [expression]}
        """
        if call['classvar']:
            self.vmfile.write(f"push {self.getSegment(call['classvar'])} {self.getIndex(call['classvar'])}\n")
            self.vmfile.write(f"call {call['classvar']}.{call['name']} {len(call['argument']) + 1}\n")
        else:
            self.vmfile.write(f"call {call['name']} {len(call['argument'])}\n")
        def error(self, message=''):
            print(f"SyntaxError: {message}")
            exit()


if __name__ == '__main__':
    file = sys.argv[1]
    print('-----debut')
    generator = Generator(file)
    generator.jackclass()
    print('-----fin')
