"""
Simple Language Interpreter

This module provides a complete interpreter for the custom language,
combining lexer, parser, and interpreter functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lexer import Lexer, TokenType
from parser import Parser
from interpreter import Interpreter as InterpreterEngine
from ast_nodes import ASTPrinter

class LanguageInterpreter:
    """
    Main interpreter class that combines all components.
    """
    
    def __init__(self, debug=False):
        """
        Initialize the interpreter.
        
        Args:
            debug (bool): Enable debug output
        """
        self.debug = debug
        self.interpreter = InterpreterEngine()
    
    def run(self, source_code: str):
        """
        Run source code through the complete pipeline.
        
        Args:
            source_code (str): Source code to execute
            
        Returns:
            Any: Result of execution
        """
        try:
            # Lexical analysis
            if self.debug:
                print("=== LEXICAL ANALYSIS ===")
            
            lexer = Lexer(source_code)
            tokens = lexer.tokenize()
            
            if self.debug:
                print("Tokens:")
                for token in tokens:
                    if token.type not in [TokenType.NEWLINE, TokenType.COMMENT]:
                        print(f"  {token}")
                print()
            
            # Parsing
            if self.debug:
                print("=== PARSING ===")
            
            parser = Parser(tokens)
            ast = parser.parse()
            
            if self.debug:
                print("Abstract Syntax Tree:")
                printer = ASTPrinter()
                ast.accept(printer)
                print()
            
            # Interpretation
            if self.debug:
                print("=== EXECUTION ===")
            
            result = self.interpreter.interpret(ast)
            
            if self.debug:
                print(f"\nExecution completed. Result: {result}")
            
            return result
            
        except Exception as e:
            print(f"Error: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
            return None
    
    def run_file(self, filename: str):
        """
        Run a source file.
        
        Args:
            filename (str): Path to source file
        """
        try:
            with open(filename, 'r') as file:
                source_code = file.read()
            
            print(f"Running file: {filename}")
            print("=" * 50)
            
            return self.run(source_code)
            
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return None
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    
    def repl(self):
        """
        Start an interactive Read-Eval-Print Loop.
        """
        print("Simple Language Interpreter")
        print("Type 'exit' to quit, 'debug on/off' to toggle debug mode")
        print("=" * 50)
        
        while True:
            try:
                line = input(">>> ").strip()
                
                if line.lower() == 'exit':
                    print("Goodbye!")
                    break
                
                if line.lower() == 'debug on':
                    self.debug = True
                    print("Debug mode enabled")
                    continue
                
                if line.lower() == 'debug off':
                    self.debug = False
                    print("Debug mode disabled")
                    continue
                
                if line.lower() == 'help':
                    self._print_help()
                    continue
                
                if not line:
                    continue
                
                # Add semicolon if missing for single expressions
                if not line.endswith(';') and not line.endswith('}'):
                    line += ';'
                
                result = self.run(line)
                
                if result is not None:
                    print(f"Result: {result}")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def _print_help(self):
        """Print help information."""
        help_text = """
Available commands:
  exit          - Exit the interpreter
  debug on/off  - Toggle debug mode
  help          - Show this help message

Language syntax:
  Variables:    var x = 10;
  Functions:    function add(a, b) { return a + b; }
  If-else:      if (x > 5) { print("big"); } else { print("small"); }
  While:        while (x > 0) { x = x - 1; }
  Print:        print("Hello, World!");

Examples:
  var x = 5;
  var y = x * 2;
  print(x + y);
  
  function factorial(n) {
      if (n <= 1) {
          return 1;
      } else {
          return n * factorial(n - 1);
      }
  }
  print(factorial(5));
        """
        print(help_text)

def main():
    """
    Main function for command-line usage.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple Language Interpreter")
    parser.add_argument("file", nargs="?", help="Source file to run")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    parser.add_argument("--repl", action="store_true", help="Start interactive REPL")
    
    args = parser.parse_args()
    
    interpreter = LanguageInterpreter(debug=args.debug)
    
    if args.file:
        interpreter.run_file(args.file)
    elif args.repl or not args.file:
        interpreter.repl()

if __name__ == "__main__":
    main()

