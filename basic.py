####################################
#               DIGITS
####################################

DIGITS = '0123456789'

####################################
#               ERRORS
####################################
class Error:
    def __init__(self, position_start, position_end, error_name, details):
        self.position_start = position_start
        self.position_end = position_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f'File {self.position_start.file_name}, line {self.position_start.ln + 1}'
        return result

class IllegalCharError(Error):
    def __init__(self, position_start, position_end, details):
        super().__init__(position_start, position_end, 'Illegal Character', details)

#####################################
#           POSITION
#####################################   

class Position:
    def __init__(self, index, ln, column, file_name, file_text):
        self.index = index
        self.ln = ln
        self.column = column
        self.file_name = file_name
        self.file_text = file_text
    
    def advance(self, current_char):
        self.index += 1
        self.column += 1

        if current_char == '\n':
            self.ln += 1
            self.column = 0

        return self
    
    def copy(self):
        return Position(self.index, self.ln, self.column, self.file_name, self.file_text)

#####################################
#      TOKENS
#####################################
TT_INT     = 'TT_INT'
TT_FLOAT   = 'FLOAT'
TT_PLUS    = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL     = 'MUL'
TT_DIV     = 'DIV'
TT_LPAREN  = 'LPAREN'
TT_RPAREN  = 'RPAREN'

class Token:
    def __init__(self, type_, value = None):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        if self.value : return f'{self.type}:{self.value}'
        return f'{self.type}'
    
#####################################
#             LEXER
#####################################
    
class Lexer:
    def __init__(self, file_name, text):
        self.file_name = file_name
        self.text = text
        self.pos  = Position(-1, 0, -1, file_name, text)
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else :
                position_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(position_start,self.pos, "'" + char + "'")

        return tokens, None
    
    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break 
                dot_count += 1
                num_str += '.'
            
            else :
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else: 
            return Token(TT_FLOAT, float(num_str))
        
###########################################
#               RUN
###########################################
        
def run(file_name, text):
    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()

    return tokens, error