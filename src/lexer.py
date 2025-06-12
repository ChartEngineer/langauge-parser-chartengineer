"""
Lexical Analyzer (Tokenizer) for the Custom Language

This module breaks down source code into tokens for parsing.
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Iterator

class TokenType(Enum):
    """Token types for the language."""
    # Literals
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    IDENTIFIER = auto()
    
    # Keywords
    VAR = auto()
    FUNCTION = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    RETURN = auto()
    TRUE = auto()
    FALSE = auto()
    NULL = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    ASSIGN = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_THAN = auto()
    GREATER_EQUAL = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Delimiters
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    COMMA = auto()
    SEMICOLON = auto()
    DOT = auto()
    
    # Special
    NEWLINE = auto()
    EOF = auto()
    COMMENT = auto()

@dataclass
class Token:
    """Represents a token in the source code."""
    type: TokenType
    value: str
    line: int
    column: int
    
    def __str__(self):
        return f"Token({self.type.name}, '{self.value}', {self.line}:{self.column})"

class LexerError(Exception):
    """Exception raised by the lexer."""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Lexer error at {line}:{column}: {message}")

class Lexer:
    """
    Lexical analyzer for the custom programming language.
    """
    
    # Keywords mapping
    KEYWORDS = {
        'var': TokenType.VAR,
        'function': TokenType.FUNCTION,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'for': TokenType.FOR,
        'return': TokenType.RETURN,
        'true': TokenType.TRUE,
        'false': TokenType.FALSE,
        'null': TokenType.NULL,
        'and': TokenType.AND,
        'or': TokenType.OR,
        'not': TokenType.NOT,
    }
    
    # Single character tokens
    SINGLE_CHAR_TOKENS = {
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.MULTIPLY,
        '/': TokenType.DIVIDE,
        '%': TokenType.MODULO,
        '(': TokenType.LEFT_PAREN,
        ')': TokenType.RIGHT_PAREN,
        '{': TokenType.LEFT_BRACE,
        '}': TokenType.RIGHT_BRACE,
        '[': TokenType.LEFT_BRACKET,
        ']': TokenType.RIGHT_BRACKET,
        ',': TokenType.COMMA,
        ';': TokenType.SEMICOLON,
        '.': TokenType.DOT,
    }
    
    def __init__(self, source: str):
        """
        Initialize the lexer with source code.
        
        Args:
            source (str): Source code to tokenize
        """
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
    
    def current_char(self) -> Optional[str]:
        """Get the current character."""
        if self.position >= len(self.source):
            return None
        return self.source[self.position]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Peek at a character ahead."""
        pos = self.position + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self) -> Optional[str]:
        """Advance to the next character."""
        if self.position >= len(self.source):
            return None
        
        char = self.source[self.position]
        self.position += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        return char
    
    def skip_whitespace(self):
        """Skip whitespace characters except newlines."""
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def read_number(self) -> Token:
        """Read a number token."""
        start_column = self.column
        value = ''
        has_dot = False
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if has_dot:
                    break  # Second dot, stop here
                has_dot = True
            value += self.current_char()
            self.advance()
        
        return Token(TokenType.NUMBER, value, self.line, start_column)
    
    def read_string(self) -> Token:
        """Read a string token."""
        start_column = self.column
        quote_char = self.current_char()
        self.advance()  # Skip opening quote
        
        value = ''
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                self.advance()
                # Handle escape sequences
                escape_char = self.current_char()
                if escape_char == 'n':
                    value += '\n'
                elif escape_char == 't':
                    value += '\t'
                elif escape_char == 'r':
                    value += '\r'
                elif escape_char == '\\':
                    value += '\\'
                elif escape_char == quote_char:
                    value += quote_char
                else:
                    value += escape_char
                self.advance()
            else:
                value += self.current_char()
                self.advance()
        
        if not self.current_char():
            raise LexerError("Unterminated string", self.line, start_column)
        
        self.advance()  # Skip closing quote
        return Token(TokenType.STRING, value, self.line, start_column)
    
    def read_identifier(self) -> Token:
        """Read an identifier or keyword token."""
        start_column = self.column
        value = ''
        
        while (self.current_char() and 
               (self.current_char().isalnum() or self.current_char() == '_')):
            value += self.current_char()
            self.advance()
        
        # Check if it's a keyword
        token_type = self.KEYWORDS.get(value, TokenType.IDENTIFIER)
        return Token(token_type, value, self.line, start_column)
    
    def read_comment(self) -> Token:
        """Read a comment token."""
        start_column = self.column
        value = ''
        
        # Skip the '//'
        self.advance()
        self.advance()
        
        # Read until end of line
        while self.current_char() and self.current_char() != '\n':
            value += self.current_char()
            self.advance()
        
        return Token(TokenType.COMMENT, value.strip(), self.line, start_column)
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize the entire source code.
        
        Returns:
            List[Token]: List of tokens
        """
        self.tokens = []
        
        while self.current_char():
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            char = self.current_char()
            
            # Newlines
            if char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, char, self.line, self.column))
                self.advance()
                continue
            
            # Numbers
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Strings
            if char in '"\'':
                self.tokens.append(self.read_string())
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Comments
            if char == '/' and self.peek_char() == '/':
                self.tokens.append(self.read_comment())
                continue
            
            # Two-character operators
            if char == '=' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.EQUAL, '==', self.line, self.column))
                self.advance()
                self.advance()
                continue
            
            if char == '!' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.NOT_EQUAL, '!=', self.line, self.column))
                self.advance()
                self.advance()
                continue
            
            if char == '<' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', self.line, self.column))
                self.advance()
                self.advance()
                continue
            
            if char == '>' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', self.line, self.column))
                self.advance()
                self.advance()
                continue
            
            # Single character operators
            if char in self.SINGLE_CHAR_TOKENS:
                token_type = self.SINGLE_CHAR_TOKENS[char]
                self.tokens.append(Token(token_type, char, self.line, self.column))
                self.advance()
                continue
            
            # Assignment operator
            if char == '=':
                self.tokens.append(Token(TokenType.ASSIGN, char, self.line, self.column))
                self.advance()
                continue
            
            # Comparison operators
            if char == '<':
                self.tokens.append(Token(TokenType.LESS_THAN, char, self.line, self.column))
                self.advance()
                continue
            
            if char == '>':
                self.tokens.append(Token(TokenType.GREATER_THAN, char, self.line, self.column))
                self.advance()
                continue
            
            # Unknown character
            raise LexerError(f"Unexpected character '{char}'", self.line, self.column)
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens
    
    def print_tokens(self):
        """Print all tokens for debugging."""
        for token in self.tokens:
            if token.type not in [TokenType.NEWLINE, TokenType.COMMENT]:
                print(token)

def main():
    """
    Test the lexer with sample code.
    """
    sample_code = '''
    // Sample program
    var x = 10;
    var y = "Hello, World!";
    
    function factorial(n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }
    
    var result = factorial(5);
    print(result);
    '''
    
    print("Tokenizing sample code:")
    print("=" * 50)
    print(sample_code)
    print("=" * 50)
    
    lexer = Lexer(sample_code)
    tokens = lexer.tokenize()
    
    print("Tokens:")
    lexer.print_tokens()
    
    print(f"\nTotal tokens: {len(tokens)}")

if __name__ == "__main__":
    main()

