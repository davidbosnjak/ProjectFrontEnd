#######################################
# IMPORTS
#######################################

from lexer import *
from parser import *
import pickle
import os
#######################################
# ERRORS
#######################################


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f"{self.error_name}: {self.details}\n"
        result += f"File {self.pos_start.fn}, line {self.pos_start.ln + 1}"
        result += "\n\n" + string_with_arrows(
            self.pos_start.ftxt, self.pos_start, self.pos_end
        )
        return result

#if lexer sees a character it doesnt recognize
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal Character", details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=""):
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)
class RunTimeError(Error):
    def __init__(self, pos_start, pos_end, description, context):
        super().__init__(pos_start, pos_end, "Runtime Error: ",description)
        self.context = context
    
    def as_string(self):
        result = self.generate_traceback()
        result += f"{self.error_name}: {self.details}\n"
        result += "\n\n" + string_with_arrows(
            self.pos_start.ftxt, self.pos_start, self.pos_end
        )
        return result
    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        context = self.context
        while context:
            result = f'File {pos.fn}, line{str(pos.ln+1)}, in {context.display_name}\n'
            pos = context.parent_entry_pos
            context = context.parent
        return 'Traceback (most recent call last):\n'+result

    


def string_with_arrows(text, pos_start, pos_end):
    result = ''

    # Calculate indices
    idx_start = max(text.rfind('\n', 0, pos_start.idx), 0)
    idx_end = text.find('\n', idx_start + 1)
    if idx_end < 0: idx_end = len(text)
    
    # Generate each line
    line_count = pos_end.ln - pos_start.ln + 1
    for i in range(line_count):
        # Calculate line columns
        line = text[idx_start:idx_end]
        col_start = pos_start.col if i == 0 else 0
        col_end = pos_end.col if i == line_count - 1 else len(line) - 1

        # Append to result
        result += line + '\n'
        result += ' ' * col_start + '^' * (col_end - col_start)

        # Re-calculate indices
        idx_start = idx_end
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0: idx_end = len(text)

    return result.replace('\t', '')

#runtime result class to keep track of the runtime result

class RunTimeResult:
    def __init__(self):
        self.value = None
        self.error = None
    def register(self, res):
        if res.error: self.error = res.error
        return res.value
    def success(self, value):
        self.value = value
        return self
    def failure(self, error):
        self.error = error
        return self



 #interpreter
class List:
    def __init__(self, elements):
        self.set_pos()
        self.set_context()
        self.elements = elements
    def added_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None
    def concat_list(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
    def remove_from_list(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RunTimeError(other.pos_start, other.pos_end, "Out of bounds index", self.context)
        else: 
            return None, RunTimeError(other.pos_start, other.pos_end, "Illegal operation", self.context)

    def get_index(self, other):
        if isinstance(other, List):
            try:
                return self.elements[other.value], None
            except:
                return None, RunTimeError(other.pos_start, other.pos_end, "Out of bounds index", self.context)
        else: 
            return None, RunTimeError(other.pos_start, other.pos_end, "Illegal operation", self.context)
    def copy(self):
        copy = List(self.elements[:])
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    def set_context(self, context=None):
        self.context = context
        return self
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
    def __repr__(self):
        return f'[{",".join([str(x) for x in self.elements])}]'
class Number:
    def __init__(self, value):

        self.value = value
        self.set_pos()
        self.set_context()
    def set_context(self, context=None):
        self.context = context
        return self
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
    def added_to(self, other):
        if isinstance(other, Number):
            num = Number(self.value+other.value)
            num.set_context(self.context)
            return num, None
    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value-other.value).set_context(self.context), None
    def mult_by(self, other):
        if isinstance(other, Number):
            return Number(self.value*other.value).set_context(self.context), None
    def div_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(other.pos_start, other.pos_end, "Division by Zero", self.context)
            return Number(self.value/other.value).set_context(self.context), None
    def powed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value**other.value).set_context(self.context), None
    def equal_to(self, other):
        if isinstance(other, Number):
            return Boolean(self.value == other.value).set_context(self.context), None
    def greater_than(self, other):
        if isinstance(other, Number):
            return Boolean(self.value > other.value).set_context(self.context), None
    def greater_than_eq(self, other):
        if isinstance(other, Number):
            return Boolean(self.value >= other.value).set_context(self.context), None
    def less_than(self, other):
        if isinstance(other, Number):
            return Boolean(self.value < other.value).set_context(self.context), None
    def less_than_eq(self, other):
        if isinstance(other, Number):
            return Boolean(self.value <= other.value).set_context(self.context), None
    def not_eq(self, other):
        if isinstance(other, Number):
            return Boolean(self.value!=other.value).set_context(self.context), None

    def is_true(self):
        return self.value !=0
     
    def __repr__(self):
        return str(self.value)

class Boolean:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_context(self, context=None):
        self.context = context 
        return self
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end 
    def is_true(self):
        return self.value =="True" or self.value ==True
    def equal_to(self, other):
        if isinstance(other, Boolean):
            return Boolean(self.value == other.value).set_context(self.context), None
    def is_and(self, other):
        self.fix_values(other)

        if isinstance(other, Boolean):

            return Boolean(self.value and other.value).set_context(self.context), None
    def is_or(self, other):
        if isinstance(other, Boolean):
            self.fix_values(other)
            
            return Boolean(self.value or other.value).set_context(self.context), None
    def fix_values(self, other):
        if other.value == "False": other.value = False
        if other.value == "True" : other.value = True
        if self.value == "True": self.value = True
        if self.value == "False": self.value = False
    def is_xor(self, other):
        self.fix_values(other)

        if isinstance(other, Boolean):
            return Boolean(self.value!=other.value).set_context(self.context), None
    def __repr__(self):
        return str(self.value)

class String:
    def __init__(self, value):

        self.value = value
        self.set_pos()
        self.set_context()

    def set_context(self, context=None):
        self.context = context
        return self
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
    def __repr__(self):
        return str(self.value)

class Char:
    def __init__(self, value):

        self.value = value
        self.set_pos()
        self.set_context()

    def set_context(self, context=None):
        self.context = context
        return self
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
    def __repr__(self):
        return str(self.value)
class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None





#symbols

class SymbolTable:
    def __init__(self):
        #storing as hashmap
        path = os.getcwd()
        with open("src/data.txt", "rb") as file:
            try:
                self.symbols = pickle.load(file)
            except:
                self.symbols = {}
                pass
        #parent symbol table for when we have other functions. and globals
        self.parent = None
    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value
        with open("src/data.txt", "wb") as file:
            pickle.dump(self.symbols, file)
    def remove(self, name):
        
        del self.symbols[name]
        with open("src/data.txt", "wb") as file:
            pickle.dump(self.symbols, file)






#interpreter

class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):

        raise Exception(f'No visit_{type(node).__name__}')
    
    #need a visit method for each type of thing in syntax tree

    def visit_WhileNode(self, node, context):
        res = RunTimeResult()
        elements = []
        while True: 
            condition = res.register(self.visit(node.condition_node, context))
            if res.error: return res
            if not condition.is_true(): break
            elements.append(res.register(self.visit(node.body_node, context)))
            if res.error: return res
        
        my_list = List(elements)
        my_list.set_context(context)
        my_list.set_pos(node.pos_start, node.pos_end)
        return res.success(my_list)
    def visit_ForNode(self, node, context):
        res = RunTimeResult()
        elements = []


        end_value = lambda : res.register(self.visit(node.end_value_node, context))
        #print(end_value().value)
        if res.error: return res

        step_value = lambda: res.register(self.visit(node.step_value_node, context))
        if res.error: return result
        
        while end_value().value:
            
            step_value()
            elements.append(res.register(self.visit(node.body_node, context)))
            if res.error: return res
        my_list = List(elements)
        my_list.set_context(context)
        my_list.set_pos(node.pos_start, node.pos_end)
        return res.success(my_list)

    def visit_BooleanNode(self, node, context):
        boolean = Boolean(node.tok.value)
        boolean.set_pos(node.pos_start, node.pos_end)
        boolean.set_context(context)
        return RunTimeResult().success(boolean)
    def visit_VarAccessNode(self, node, context):
        res = RunTimeResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)
        #if the value is not in the symbol table
        if not value: 
            return res.failure(RunTimeError(node.pos_start, node.pos_end, f"'{var_name}' is not defined", context))

        return res.success(value)
    def visit_CharNode(self, node, context):
        char = Char(node.tok.value)
        char.set_pos(node.pos_start, node.pos_end)
        char.set_context(context)
        return RunTimeResult().success(char)
    def visit_StringNode(self, node, context):
        literal = String(node.tok.value)
        literal.set_pos(node.pos_start, node.pos_end)
        literal.set_context(context)
        return RunTimeResult().success(literal)

    def visit_ListNode(self, node, context):
        res = RunTimeResult()
        elements = []
        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.error: return res

        my_list = List(elements)
        my_list.set_context(context)
        my_list.set_pos(node.pos_start, node.pos_end)
        
        return res.success(my_list)

    def visit_VarIncrementNode(self, node, context):
        res = RunTimeResult()
        var_name = node.var_name_tok.value
        correct_symbol = context.symbol_table.get(var_name)
        if not correct_symbol: return res.failure(RunTimeError(node.pos_start, node.pos_end, f"'{var_name}' must be declared first", context))

        value, error = context.symbol_table.get(var_name).added_to(Number(node.increment_value))
        context.symbol_table.remove(var_name)
        context.symbol_table.set(var_name, value)
        return res.success(value)
    def visit_VarReassignNode(self, node, context):
        res = RunTimeResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        
        if res.error: return res
        symbol_value = context.symbol_table.get(var_name)
        if not symbol_value:
            return res.failure(RunTimeError(node.pos_start, node.pos_end, f"'{var_name}' must be declared first", context))
        context.symbol_table.remove(var_name)
        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RunTimeResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res
        context.symbol_table.set(var_name, value)
        return res.success(value)
    def visit_CommentNode(self, node, context):
        return res.success(literal)
    def visit_NumberNode(self, node, context):

        number = Number(node.tok.value)
        number.set_pos(node.pos_start, node.pos_end)
        number.set_context(context)
        return RunTimeResult().success(number)
    def visit_BinOpNode(self, node, context):
        res = RunTimeResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res
        
        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_COMPARE:
            result, error = left.equal_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.mult_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.div_by(right)
        elif node.op_tok.type == TT_POWER:
            result, error =  left.powed_by(right)
        elif node.op_tok.type == TT_GREATERTHAN:
            result, error = left.greater_than(right)

        elif node.op_tok.type == TT_GREATERTHANEQ:
            result, error = left.greater_than_eq(right)
        elif node.op_tok.type == TT_LESSTHAN:
            result, error = left.less_than(right)
        elif node.op_tok.type == TT_LESSTHANEQ:
            result, error = left.less_than_eq(right)
        elif node.op_tok.type == TT_NOTEQUALTO:
            result, error = left.not_eq(right)
        elif node.op_tok.type == TT_AND:
            result, error = left.is_and(right)
        elif node.op_tok.type == TT_OR:

            result, error = left.is_or(right)
        elif node.op_tok.type == TT_XOR:
            result, error = left.is_xor(right)
        
        if error:
            return res.failure(error)
        else:
            result.set_pos(node.pos_start, node.pos_end)
        
            return res.success(result)
        

        self.visit(node.left_node)
        self.visit(node.right_node)
    def visit_UnaryOpNode(self, node, context):
        res = RunTimeResult()
        number = res.register(self.visit(node.node, context))
        if res.error:
            return res
        error = None
        if node.op_tok.type == TT_MINUS:
            number = number.mult_by(Number(-1))
        if error:
            return res.failure(error)
        else:

            return res.success(number.set_pos(node.pos_start, node.pos_end))
    def visit_IfNode(self, node, context):
        res =RunTimeResult()

        for condition, expr in node.cases:
            condition_value =res.register(self.visit(condition, context))
            if res.error: return res

            if condition_value.is_true():
                
                expr_value = res.register(self.visit(expr, context))
                if res.error: return res
                return res.success(expr_value)
        if node.else_case:
            else_value = res.register(self.visit(node.else_case, context))
            if res.error: return result
            return res.success(else_value)
        return res.success(None)


#######################################
# RUN
#######################################

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0))
def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table

    result = interpreter.visit(ast.node, context)

    
    return result.value, result.error
