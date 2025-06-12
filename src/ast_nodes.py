"""
Abstract Syntax Tree Node Definitions

This module defines the AST node classes for the language.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional
from dataclasses import dataclass

class ASTNode(ABC):
    """Base class for all AST nodes."""
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for the visitor pattern."""
        pass

# Expressions
class Expression(ASTNode):
    """Base class for all expressions."""
    pass

@dataclass
class LiteralExpression(Expression):
    """Literal value expression (numbers, strings, booleans)."""
    value: Any
    
    def accept(self, visitor):
        return visitor.visit_literal_expression(self)

@dataclass
class IdentifierExpression(Expression):
    """Variable identifier expression."""
    name: str
    
    def accept(self, visitor):
        return visitor.visit_identifier_expression(self)

@dataclass
class BinaryExpression(Expression):
    """Binary operation expression (e.g., a + b)."""
    left: Expression
    operator: str
    right: Expression
    
    def accept(self, visitor):
        return visitor.visit_binary_expression(self)

@dataclass
class UnaryExpression(Expression):
    """Unary operation expression (e.g., -a, !b)."""
    operator: str
    operand: Expression
    
    def accept(self, visitor):
        return visitor.visit_unary_expression(self)

@dataclass
class CallExpression(Expression):
    """Function call expression."""
    callee: Expression
    arguments: List[Expression]
    
    def accept(self, visitor):
        return visitor.visit_call_expression(self)

@dataclass
class AssignmentExpression(Expression):
    """Assignment expression (e.g., x = 5)."""
    name: str
    value: Expression
    
    def accept(self, visitor):
        return visitor.visit_assignment_expression(self)

# Statements
class Statement(ASTNode):
    """Base class for all statements."""
    pass

@dataclass
class ExpressionStatement(Statement):
    """Expression used as a statement."""
    expression: Expression
    
    def accept(self, visitor):
        return visitor.visit_expression_statement(self)

@dataclass
class VarStatement(Statement):
    """Variable declaration statement."""
    name: str
    initializer: Optional[Expression] = None
    
    def accept(self, visitor):
        return visitor.visit_var_statement(self)

@dataclass
class BlockStatement(Statement):
    """Block of statements."""
    statements: List[Statement]
    
    def accept(self, visitor):
        return visitor.visit_block_statement(self)

@dataclass
class IfStatement(Statement):
    """If-else statement."""
    condition: Expression
    then_branch: Statement
    else_branch: Optional[Statement] = None
    
    def accept(self, visitor):
        return visitor.visit_if_statement(self)

@dataclass
class WhileStatement(Statement):
    """While loop statement."""
    condition: Expression
    body: Statement
    
    def accept(self, visitor):
        return visitor.visit_while_statement(self)

@dataclass
class FunctionStatement(Statement):
    """Function declaration statement."""
    name: str
    parameters: List[str]
    body: List[Statement]
    
    def accept(self, visitor):
        return visitor.visit_function_statement(self)

@dataclass
class ReturnStatement(Statement):
    """Return statement."""
    value: Optional[Expression] = None
    
    def accept(self, visitor):
        return visitor.visit_return_statement(self)

@dataclass
class PrintStatement(Statement):
    """Print statement (built-in)."""
    expression: Expression
    
    def accept(self, visitor):
        return visitor.visit_print_statement(self)

# Program
@dataclass
class Program(ASTNode):
    """Root node representing the entire program."""
    statements: List[Statement]
    
    def accept(self, visitor):
        return visitor.visit_program(self)

# Visitor interface
class Visitor(ABC):
    """Visitor interface for traversing the AST."""
    
    @abstractmethod
    def visit_literal_expression(self, expr: LiteralExpression):
        pass
    
    @abstractmethod
    def visit_identifier_expression(self, expr: IdentifierExpression):
        pass
    
    @abstractmethod
    def visit_binary_expression(self, expr: BinaryExpression):
        pass
    
    @abstractmethod
    def visit_unary_expression(self, expr: UnaryExpression):
        pass
    
    @abstractmethod
    def visit_call_expression(self, expr: CallExpression):
        pass
    
    @abstractmethod
    def visit_assignment_expression(self, expr: AssignmentExpression):
        pass
    
    @abstractmethod
    def visit_expression_statement(self, stmt: ExpressionStatement):
        pass
    
    @abstractmethod
    def visit_var_statement(self, stmt: VarStatement):
        pass
    
    @abstractmethod
    def visit_block_statement(self, stmt: BlockStatement):
        pass
    
    @abstractmethod
    def visit_if_statement(self, stmt: IfStatement):
        pass
    
    @abstractmethod
    def visit_while_statement(self, stmt: WhileStatement):
        pass
    
    @abstractmethod
    def visit_function_statement(self, stmt: FunctionStatement):
        pass
    
    @abstractmethod
    def visit_return_statement(self, stmt: ReturnStatement):
        pass
    
    @abstractmethod
    def visit_print_statement(self, stmt: PrintStatement):
        pass
    
    @abstractmethod
    def visit_program(self, program: Program):
        pass

class ASTPrinter(Visitor):
    """Visitor that prints the AST structure."""
    
    def __init__(self):
        self.indent_level = 0
    
    def _indent(self):
        return "  " * self.indent_level
    
    def _print_with_indent(self, text):
        print(f"{self._indent()}{text}")
    
    def visit_literal_expression(self, expr: LiteralExpression):
        self._print_with_indent(f"Literal: {repr(expr.value)}")
    
    def visit_identifier_expression(self, expr: IdentifierExpression):
        self._print_with_indent(f"Identifier: {expr.name}")
    
    def visit_binary_expression(self, expr: BinaryExpression):
        self._print_with_indent(f"Binary: {expr.operator}")
        self.indent_level += 1
        expr.left.accept(self)
        expr.right.accept(self)
        self.indent_level -= 1
    
    def visit_unary_expression(self, expr: UnaryExpression):
        self._print_with_indent(f"Unary: {expr.operator}")
        self.indent_level += 1
        expr.operand.accept(self)
        self.indent_level -= 1
    
    def visit_call_expression(self, expr: CallExpression):
        self._print_with_indent("Call:")
        self.indent_level += 1
        expr.callee.accept(self)
        for arg in expr.arguments:
            arg.accept(self)
        self.indent_level -= 1
    
    def visit_assignment_expression(self, expr: AssignmentExpression):
        self._print_with_indent(f"Assignment: {expr.name}")
        self.indent_level += 1
        expr.value.accept(self)
        self.indent_level -= 1
    
    def visit_expression_statement(self, stmt: ExpressionStatement):
        self._print_with_indent("Expression Statement:")
        self.indent_level += 1
        stmt.expression.accept(self)
        self.indent_level -= 1
    
    def visit_var_statement(self, stmt: VarStatement):
        self._print_with_indent(f"Var: {stmt.name}")
        if stmt.initializer:
            self.indent_level += 1
            stmt.initializer.accept(self)
            self.indent_level -= 1
    
    def visit_block_statement(self, stmt: BlockStatement):
        self._print_with_indent("Block:")
        self.indent_level += 1
        for statement in stmt.statements:
            statement.accept(self)
        self.indent_level -= 1
    
    def visit_if_statement(self, stmt: IfStatement):
        self._print_with_indent("If:")
        self.indent_level += 1
        self._print_with_indent("Condition:")
        self.indent_level += 1
        stmt.condition.accept(self)
        self.indent_level -= 1
        self._print_with_indent("Then:")
        self.indent_level += 1
        stmt.then_branch.accept(self)
        self.indent_level -= 1
        if stmt.else_branch:
            self._print_with_indent("Else:")
            self.indent_level += 1
            stmt.else_branch.accept(self)
            self.indent_level -= 1
        self.indent_level -= 1
    
    def visit_while_statement(self, stmt: WhileStatement):
        self._print_with_indent("While:")
        self.indent_level += 1
        self._print_with_indent("Condition:")
        self.indent_level += 1
        stmt.condition.accept(self)
        self.indent_level -= 1
        self._print_with_indent("Body:")
        self.indent_level += 1
        stmt.body.accept(self)
        self.indent_level -= 1
        self.indent_level -= 1
    
    def visit_function_statement(self, stmt: FunctionStatement):
        params = ", ".join(stmt.parameters)
        self._print_with_indent(f"Function: {stmt.name}({params})")
        self.indent_level += 1
        for statement in stmt.body:
            statement.accept(self)
        self.indent_level -= 1
    
    def visit_return_statement(self, stmt: ReturnStatement):
        self._print_with_indent("Return:")
        if stmt.value:
            self.indent_level += 1
            stmt.value.accept(self)
            self.indent_level -= 1
    
    def visit_print_statement(self, stmt: PrintStatement):
        self._print_with_indent("Print:")
        self.indent_level += 1
        stmt.expression.accept(self)
        self.indent_level -= 1
    
    def visit_program(self, program: Program):
        self._print_with_indent("Program:")
        self.indent_level += 1
        for statement in program.statements:
            statement.accept(self)
        self.indent_level -= 1

