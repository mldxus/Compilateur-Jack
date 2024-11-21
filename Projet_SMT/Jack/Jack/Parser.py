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
       #while self.lexer.hasNext() and self.lexer.look()['token'] in {'static', 'field'}:
           #self.classVarDec()
       self.process('}')
       return {
           'line': line,
           'col': col,
           'type': 'class',
           'name': className,
           'classVarDecs': [self.classVarDec()],
           'subroutines': [self.subroutineDec()]
}


   def classVarDec(self):
       """
       classVarDec: ('static'| 'field') type varName (',' varName)* ';'
       """
       line = self.lexer.look()['line']
       col = self.lexer.look()['col']
       if self.lexer.look()['token'] == 'static' :
           kind = 'static'
       else :
           kind = 'this'
       self.process(self.lexer.look()['token'])
       type = self.type()
       varName = []
       varName.append(self.varName())
       while self.lexer.look()['token'] == ',':
           self.process(',')
           varName.append(self.varName())
       self.process(';')
       return {'line':line, 'col':col, 'name':varName, 'kind':kind, 'type':type}


   def type(self):
       """
       type: 'int'|'char'|'boolean'|className
       """
       return 'Todo'




   def subroutineDec(self):
       """
       subroutineDec: ('constructor'| 'function'|'method') ('void'|type)
       subroutineName '(' parameterList ')' subroutineBody
       """
       line = self.lexer.look()['line']
       col = self.lexer.look()['col']
       token = self.lexer.token()
       match token['keyword']:
           case 'constructor':
               type = self.process('constructor')
           case 'function':
               type = self.process('function')
           case 'method':
               type = self.process('method')
       if token['keyword'] == 'void':
           retourne = self.process('void')
       else:
           retourne = self.type()
       name = self.subroutineName()
       self.process('(')
       self.parameterList()
       self.process(')')
       self.subroutineBody()
       return {'line':line, 'col':col, 'type':type, 'return':retourne, 'name':name, 'argument':[], 'local': [], 'instructions':[self.statements()]}


   def parameterList(self):
       """
       parameterList: ((type varName) (',' type varName)*)?
       """
       return 'Todo'


   def subroutineBody(self):
       """
       subroutineBody: '{' varDec* statements '}'
       """
       return 'Todo'


   def varDec(self):
       """
       varDec: 'var' type varName (',' varName)* ';'
       """


   def className(self):
       """
       className: identifier
       """


       token = self.lexer.next()
       if token['type'] == 'identifier':
           return token
       else:
           self.error(token)






   def subroutineName(self):
       """
       subroutineName: identifier
       """
       return 'Todo'


   def varName(self):
       """
       varName: identifier
       """
       return 'Todo'


   def statements(self):
       """
       statements : statements*
       """
       line = self.lexer.look()['line']
       col = self.lexer.look()['col']
       while self.lexer.hasNext() and self.lexer.look()['token'] in {'let','if','while','do','return'}:
           self.statement()
       return 'Todo'


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
       """
       letStatement : 'let' varName ('[' expression ']')? '=' expression ';'
       """
       line = self.lexer.look()['line']
       col = self.lexer.look()['col']
       self.process('let')
       variable = self.varName()
       if self.lexer.look()['token'] == '[':
           self.process('[')
           indice = self.expression()
           self.process(']')
       self.process('=')
       valeur = self.expression()
       self.process(';')
       return {'line':line, 'col':col, 'type':'let', 'variable':variable, 'indice':indice, 'valeur':valeur}


   def ifStatement(self):
       """
       ifStatement : 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
       """
       line = self.lexer.look()['line']
       col = self.lexer.look()['col']
       self.process('if')
       self.process('(')
       cond = self.expression()
       self.process(')')
       self.process('{')
       vrai = self.statements()
       self.process('}')
       if self.lexer.look()['token'] == 'else':
           self.process('else')
           self.process('{')
           faux = self.statements()
           self.process('}')
       return {'line':line, 'col':col, 'type':'if', 'condition':cond, 'true':[vrai], 'false':[faux]}


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
       """
       doStatement : 'do' subroutineCall ';'
       """
       self.process('do')
       self.subroutineCall()
       self.process(';')
       return ''


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
       """
       term : integerConstant|stringConstant|keywordConstant
               |varName|varName '[' expression ']'|subroutineCall
               | '(' expression ')' | unaryOp term
       """
       return 'Todo'


   def subroutineCall(self):
       """
       subroutineCall : subroutineName '(' expressionList ')'
               | (className|varName) '.' subroutineName '(' expressionList ')'
       Attention : l'analyse syntaxique ne peut pas distingué className et varName.
           Nous utiliserons la balise <classvarName> pour (className|varName)
       """
       return 'Todo'


   def expressionList(self):
       """
       expressionList : (expression (',' expression)*)?
       """
       return 'Todo'


   def op(self):
       """
       op : '+'|'-'|'*'|'/'|'&'|'|'|'<'|'>'|'='
       """


   def unaryOp(self):
       """
       unaryop : '-'|'~'
       """
       return 'Todo'


   def KeywordConstant(self):
       """
       KeyWordConstant : 'true'|'false'|'null'|'this'
       """


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







