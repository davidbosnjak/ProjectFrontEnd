import string


DIGITS = "0123456789"

LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS+DIGITS
#######################################
# POSITION
#######################################


class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == "\n":
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


#######################################
# TOKENS
#######################################

TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_LBRAC = "LBRAC"
TT_RBRAC = "RBRAC"
TT_EOF = "EOF"
TT_INT = "INT"
TT_LITERAL = "LITERAL"
TT_IDENTIFIER = "IDENTIFIER"
TT_ASSIGNMENT = "EQUALS"
TT_TYPEKEYWORD = "TYPEKEYWORD"
TT_POWER = "POWER"
TT_DOUBLEQUOTE = "DOUBLEQUOTE"
TT_SINGLEQUOTE = "SINGLEQUOTE"
TT_SEMICOLON = "SEMICOLON"
TT_CHAR = "CHAR"
TT_COMPARE = "COMPARE"
TT_BOOL = "BOOL"
TT_KEYWORD = "KEYWORD"
TT_BUILTFUNC = "BUILTFUNC"
TT_GREATERTHAN = "GREATERTHAN"
TT_LESSTHAN = "LESSTHAN"
TT_GREATERTHANEQ = "GREATERTHANEQ"
TT_LESSTHANEQ = "LESSTHANEQ"
TT_NOTEQUALTO = "NOTEQUALTO"
TT_COMMENT = "COMMENT"
TT_AND = "and"
TT_OR = "or"
TT_XOR = "xor"
TT_NOT = "not"
TT_INCREMENT = "INCREMENT"
TT_INCREMENT_BY = "INCREMENT_BY"
TT_COMMA = "COMMA"
TT_COMMENT = "COMMENT"



#values for TYPEKEYWORD
typeValues = ["char","string", "int", "bool"]

#values for KEYWORD
keywords = ["if", "for", "while", "elif", "else"]

#values for BUILTFUNC
builtFuncs = ["print"]

class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end

    def __repr__(self):
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"
    def matches(self, type_, value):
        return self.type == type_ and self.value == value
    def matchesList(self, type_, listValue):
        if self.value in listValue and self.type == type_: return True
        else: return False


#######################################
# LEXER
#######################################


class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
    def next_tok(self):
        next_char = (self.text[self.pos.idx+1] if pos.idx+1<len(self.text)else None)
        return next_char
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = (
            self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        )

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in " \t":
                self.advance()
            elif self.current_char == "'":
                self.advance()
                tokens.append(Token(TT_CHAR, self.current_char, pos_start = self.pos))
                self.advance()
                self.advance()
            elif self.current_char == "!":
                self.advance()
                if self.current_char == "=":
                    tokens.append(Token(TT_NOTEQUALTO, pos_start=self.pos))
                    self.advance()
            elif self.current_char == "[":
                tokens.append(Token(TT_LBRAC, pos_start=self.pos))
                self.advance()
            elif self.current_char =="]":
                tokens.append(Token(TT_RBRAC, pos_start=self.pos))
                self.advance()
            elif self.current_char ==",":
                tokens.append(Token(TT_COMMA, pos_start = self.pos))
                self.advance()
            elif self.current_char == "#":
                while self.current_char !=None:
                    
                    self.advance()
            elif self.current_char ==">":
                self.advance()
                if self.current_char!= "=":

                    tokens.append(Token(TT_GREATERTHAN, pos_start=self.pos))
                else:
                    tokens.append(Token(TT_GREATERTHANEQ, pos_start=self.pos))
                    self.advance()
            elif self.current_char == "<":
                self.advance()
                if self.current_char!="=":
                    tokens.append(Token(TT_LESSTHAN, pos_start=self.pos))
                else: 
                    tokens.append(Token(TT_GREATERTHANEQ, pos_start=self.pos))
                    self.advance()
            
            elif self.current_char == ";":
                tokens.append(Token(TT_SEMICOLON, pos_start=self.pos))
                self.advance()
            elif self.current_char in LETTERS:
                tokens.append(self.make_word())
            elif self .current_char == '"':
                tokens.append(self.make_literal())
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == "+":
                   
                self.advance()
                if self.current_char == "+":
                    tokens.append(Token(TT_INCREMENT, pos_start=self.pos))
                    self.advance()
                elif self.current_char == "=":
                    tokens.append(Token(TT_INCREMENT_BY, pos_start=self.pos))
                    self.advance()
                else: 
                    tokens.append(Token(TT_PLUS, pos_start=self.pos))
                    
                
            elif self.current_char == "^":
                tokens.append(Token(TT_POWER, pos_start =self.pos))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ")":
                start_pos = self.pos.copy()
                self.advance()

                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == "=":
                self.advance()
                if(self.current_char !="="):
                    tokens.append(Token(TT_ASSIGNMENT, pos_start=self.pos))
                else:
                    tokens.append(Token(TT_COMPARE, pos_start=self.pos))
                    self.advance()
                

            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None
    def make_word(self):
        word_str= ""
        pos_start = self.pos.copy()
        while self.current_char !=None and self.current_char in LETTERS +'_':
            word_str+=self.current_char
            self.advance()
        if word_str in typeValues:
            

            return Token(TT_TYPEKEYWORD, word_str, pos_start, self.pos)
        elif word_str in ("True", "False"):
            return Token(TT_BOOL, word_str, pos_start, self.pos)
        elif word_str in keywords:
            return Token(TT_KEYWORD, word_str, pos_start, self.pos)
        elif word_str in (TT_XOR, TT_AND, TT_OR, TT_NOT):
            return Token(word_str, pos_start=self.pos)
        else: 
            

            return Token(TT_IDENTIFIER, word_str, pos_start, self.pos)
   
    def make_literal(self):
        word_str = ""
        pos_start = self.pos.copy()
        self.advance()
        while self.current_char!='"':
            word_str+=self.current_char
            self.advance()
        self.advance()
        return Token(TT_LITERAL, word_str, pos_start, self.pos)
    def make_number(self):
        num_str = ""
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += "."
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)
