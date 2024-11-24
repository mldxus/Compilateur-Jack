import sys
import Lexer
import todot

class Parser:
   """No comment"""


   def __init__(self, file):
       self.lexer = Lexer.Lexer(file)


   def jackclass(self):
       """
       class: 'class' className '{' classVarDec* subroutineDec* '}'
       """
      
       line=self.lexer.look()['line']
       col=self.lexer.look()['col']
       self.process('class')
       className=self.className()
       self.process('{')
       classVarDecs = []
       while self.lexer.hasNext() and self.lexer.look()['token'] in {'static', 'field'}:
            classVarDecs.append(self.classVarDec())
       subroutines = []
        while self.lexer.hasNext() and self.lexer.look()['token'] in {'constructor','function','method'} :
            subroutines.append(self.subroutineDec())
       self.process('}')
       return {
           'line': line,
           'col': col,
           'type': 'class',
           'name': className,
           'classVarDecs': classVarDecs,
           'subroutines': subroutines
        }


    def classVarDec(self):
        line = self.lexer.look()['line']
        col = self.lexer.look()['col']
        kind = self.lexer.next()['token']
        var_type = self.type()
        var_names = [self.varName()]

        while self.lexer.look()['token'] == ',':
            self.process(',')
            var_names.append(self.varName())

        self.process(';')
        return {
            'line': line,
            'col': col,
            'kind': kind,
            'type': var_type,
            'names': var_names
        }


       def type(self):
           """
           type: 'int'|'char'|'boolean'|className
           """
           if self.lexer.hasNext() and self.lexer.look()['token'] in {'int', 'boolean', 'char'}:
               token = self.lexer.next()
               type = token['token']
               self.xml.write(token['token'])
           elif self.lexer.hasNext() and self.lexer.look()['type'] == 'identifier':
               type = self.className()
           else:
               self.error(self.lexer.next())
           return type


    def subroutineDec(self):
        line = self.lexer.look()['line']
        col = self.lexer.look()['col']
        kind = self.lexer.next()['token']  # 'constructor', 'function', ou 'method'

        returnType = self.process('void') if self.lexer.look()['token'] == 'void' else self.type()
        name = self.subroutineName()

        self.process('(')
        parameters = self.parameterList()
        self.process(')')

        body = self.subroutineBody()

        return {
            'line': line,
            'col': col,
            'type': kind,
            'returnType': returnType,
            'name': name,
            'parameters': parameters,
            'body': body
        }


    def parameterList(self):
        params = []
        if self.lexer.look()['token'] not in {')'}:  # Si pas vide
            type = self.type()
            name = self.varName()
            params.append({'type': type, 'name': name})

            while self.lexer.look()['token'] == ',':
                self.process(',')
                type = self.type()
                name = self.varName()
                params.append({'type': type, 'name': name})
        return params


    def subroutineBody(self):
        line = self.lexer.look()['line']
        col = self.lexer.look()['col']
        self.process('{')

        varDecs = []
        while self.lexer.hasNext() and self.lexer.look()['token'] == 'var':
            varDecs.append(self.varDec())

        statements = self.statements()
        self.process('}')

        return {'line': line, 'col': col, 'type': 'subroutineBody', 'varDecs': varDecs, 'statements': statements}


    def varDec(self):
        line = self.lexer.look()['line']
        col = self.lexer.look()['col']
        self.process('var')
        var_type = self.type()
        names = [self.varName()]

        while self.lexer.look()['token'] == ',':
            self.process(',')
            names.append(self.varName())

        self.process(';')
        return {'line': line, 'col': col, 'type': 'varDec', 'varType': var_type, 'names': names}


   def className(self):
       """
       className: identifier
       """
       token = self.lexer.next()
       if token['type'] == 'identifier':
           self.xml.write(token['token'])
       else:
           self.error(token)
        return token['token']

       token = self.lexer.next()
       if token['type'] == 'identifier':
           return token
       else:
           self.error(token)


    def subroutineName(self):
        token = self.lexer.next()
        if token['type'] == 'identifier':
            return {'type': 'subroutineName', 'name': token['token']}
        else:
            self.error(token)


    def varName(self):
        token = self.lexer.next()
        if token['type'] == 'identifier':
            return {'type': 'varName', 'name': token['token']}
        else:
            self.error(token)


    def statements(self):
        stmts = []
        while self.lexer.hasNext() and self.lexer.look()['token'] in {'let', 'if', 'while', 'do', 'return'}:
            stmts.append(self.statement())
        return stmts


   def statement(self):
       """
       statement : letStatements|ifStatement|whileStatement|doStatement|returnStatement
       """
       match self.lexer.look()['token']:
           case 'if':
               self.ifStatement()
           case 'let':
               self.letStatement()
           case 'while':
               self.whileStatement()
           case 'do':
               self.doStatement()
           case 'return':
               self.returnStatement()
       return 'Todo'


    def letStatement(self):
        line = self.lexer.look()['line']
        col = self.lexer.look()['col']

        self.process('let')
        variable = self.varName()

        index = None
        if self.lexer.look()['token'] == '[':  # Tableau
            self.process('[')
            index = self.expression()
            self.process(']')

        self.process('=')
        value = self.expression()
        self.process(';')

        return {'line': line, 'col': col, 'type': 'let', 'variable': variable, 'index': index, 'value': value}


    def ifStatement(self):
        line = self.lexer.look()['line']
        col = self.lexer.look()['col']

        self.process('if')
        self.process('(')
        condition = self.expression()
        self.process(')')
        self.process('{')
        trueBlock = self.statements()
        self.process('}')

        falseBlock = None
        if self.lexer.look()['token'] == 'else':
            self.process('else')
            self.process('{')
            falseBlock = self.statements()
            self.process('}')

        return {'line': line, 'col': col, 'type': 'if', 'condition': condition, 'true': trueBlock, 'false': falseBlock}


   def whileStatement(self):
       """
       whileStatement : 'while' '(' expression ')' '{' statements '}'
       """
       line = self.lexer.look()['line']
       col = self.lexer.look()['col']
       self.process('while')
       self.process('(')
       cond = self.expression()
       self.process(')')
       self.process('{')
       inst = self.statements()
       self.process('}')
       return {'line':line, 'col':col, 'type':'while', 'condition':cond, 'instructions':[inst]}


    def doStatement(self):
        line = self.lexer.look()['line']
        col = self.lexer.look()['col']
        self.process('do')
        call = self.subroutineCall()
        self.process(';')
        return {'line': line, 'col': col, 'type': 'do', 'call': call}


   def returnStatement(self):
       """
       returnStatement : 'return' expression? ';'
       """
       line = self.lexer.look()['line']
       col = self.lexer.look()['col']
       self.process('return')
       if self.lexer.look2()['token'] == ';':
           valeur = self.expression()
       return {'line':line, 'col':col, 'type':'return', 'valeur':valeur}


   def expression(self):
       expr = [self.term()]
       while self.lexer.look()['token'] in {'+', '-', '*', '/', '&', '|', '<', '>', '='}:
           op = self.op()
           term = self.term()
           expr.extend([op, term])
       return expr


    def term(self):
        token = self.lexer.look()
        if token['type'] == 'IntegerConstant':
            return {'type': 'int', 'value': self.lexer.next()['token']}
        elif token['type'] == 'StringConstant':
            return {'type': 'string', 'value': self.lexer.next()['token']}
        elif token['token'] in {'true', 'false', 'null', 'this'}:
            return {'type': 'keyword', 'value': self.KeywordConstant()}
        elif self.lexer.look()['token'] == '(':
            self.process('(')
            expr = self.expression()
            self.process(')')
            return {'type': 'expression', 'value': expr}
        else:
            return {'type': 'var', 'name': self.varName()}


    def subroutineCall(self):
        if self.lexer.look2()['token'] == '.':
            classOrVarName = self.varName()
            self.process('.')
            subroutineName = self.subroutineName()
        else:
            classOrVarName = None
            subroutineName = self.subroutineName()

        self.process('(')
        arguments = self.expressionList()
        self.process(')')

        return {
            'classOrVar': classOrVarName,
            'subroutineName': subroutineName,
            'arguments': arguments
        }


    def expressionList(self):
        expressions = []
        if self.lexer.look()['token'] != ')':
            expressions.append(self.expression())
            while self.lexer.look()['token'] == ',':
                self.process(',')
                expressions.append(self.expression())
        return expressions


    def op(self):
        token = self.lexer.next()
        return {'type': 'operator', 'value': token['token']}


    def unaryOp(self):
        token = self.lexer.next()
        return {'type': 'unaryOp', 'value': token['token']}


    def KeywordConstant(self):
        token = self.lexer.next()
        return {'type': 'keywordConstant', 'value': token['token']}


   def process(self, str):
       token = self.lexer.next()
       if (token is not None and token['token'] == str):
           return token
       else:
           self.error(token)


   def error(self, token):
       if token is None:
           print("Syntax error: end of file")
       else:
           print(f"SyntaxError (line={token['line']}, col={token['col']}): {token['token']}")
       exit()




if __name__ == "__main__":
   if len(sys.argv) != 2:
       print("Utilisation : python3 Parser.py fichier.jack")
       sys.exit(1)


   file = sys.argv[1]
   parser = Parser(file)
   try:
       tree = parser.jackclass()
       print(tree)  # Affichage de l'arbre syntaxique simplifié
   except Exception as e:
       print(f"Erreur lors de l'analyse : {e}")







