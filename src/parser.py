
from lexer import *

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

#node definitions

class NumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end
    def __repr__(self):
        return f"{self.tok}"
class CommentNode: 
    def __init__(self):
        pass
class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

class VarAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end
class VarReassignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end
class VarIncrementNode:
    def __init__(self, var_name_tok, increment_value):
        self.var_name_tok = var_name_tok
        self.increment_value = increment_value
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end
class CharNode:
    def __init__(self, tok):
        self.tok  = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end
    def __repr__(self):
        return f"{self.tok}"
class BooleanNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end
    def __repr__(self):
        return f"{self.tok}"
class StringNode:
    def __init__(self, tok):
        self.tok  = tok
        
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end
    def __repr__(self):
        return f"{self.tok}"
class ListNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end

class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end
    def __repr__(self):
        return f"({self.left_node}, {self.op_tok}, {self.right_node})"


class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.op_tok.pos_end

    def __repr__(self):
        return f"({self.op_tok}, {self.node})"

class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case
        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[len(self.cases)-1][0]).pos_end

class ForNode:
    def __init__(self, var_name_tok,  end_value_node, step_value_node, body_node):
        self.var_name_tok = var_name_tok
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end


class WhileNode:
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node
        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end


#parse result


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node

        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

#parser


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(
        self,
    ):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok
    def unadvance(self):
        self.tok_idx-=1
        self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.boolExpr()
        if not res.error and self.current_tok.type != TT_EOF:
            #print(self.current_tok)
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected '+', '-', '*' or '/'",
                )
            )
        return res


    

    def atom(self):
        res = ParseResult()

        tok = self.current_tok
        if tok.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))
        elif tok.type == TT_COMMENT:
            while self.current_tok.type != TT_EOF:
                res.register(self.advance())
            return res.success(CommentNode())

        elif tok.type == TT_IDENTIFIER:
           
            res.register(self.advance())
            return res.success(VarAccessNode(tok))
        elif tok.type == TT_BOOL:
            res.register(self.advance())
            return res.success(BooleanNode(tok))
        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected ')'",
                    )
                )
        elif tok.type == TT_LBRAC:

            list_expr = res.register(self.list_expr())
            if res.error: return res
            return res.success(list_expr)
        elif tok.matches(TT_KEYWORD, "if"):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)
        elif tok.matches(TT_KEYWORD, "for"):
            for_expr = res.register(self.for_expr())
            if res.error: return res
            return res.success(for_expr)
        elif tok.matches(TT_KEYWORD, "while"):
            while_expr = res.register(self.while_expr())
            if res.error: return res
            return res.success(while_expr)
        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected int, float, '+','-',or '('"))

    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type == TT_RBRAC:
            res.register(self.advance())
        else:
            res.register(self.advance())
            element_nodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ']',"))
            while self.current_tok.type == TT_COMMA:
                res.register(self.advance())
                element_nodes.append(res.register(self.expr()))
                if res.error: return res
            if self.current_tok.type != TT_RBRAC:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ',' or ']' "))
            
            res.register(self.advance())
        return res.success(ListNode(element_nodes, pos_start, self.current_tok.pos_end.copy()))

    def while_expr(self):
        res = ParseResult()
        res.register(self.advance())
        if self.current_tok.type!= TT_LPAREN:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '('"))
        res.register(self.advance())
        condition = res.register(self.boolExpr())
        if res.error: return res
        if self.current_tok.type !=TT_RPAREN:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')'"))
        res.register(self.advance())
        body_expr = res.register(self.expr())
        return WhileNode(condition, body_expr)


    def for_expr(self):

        res = ParseResult()
        res.register(self.advance())
        if self.current_tok.type != TT_LPAREN:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '('"))
        res.register(self.advance())
        
        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier"))
        var_name = self.current_tok
        res.register(self.advance())
       
        if self.current_tok.type !=TT_SEMICOLON:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ';' after expression"))
        res.register(self.advance())

        stop_condition = res.register(self.boolExpr())
        if res.error: return res

        if self.current_tok.type != TT_SEMICOLON:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ';' after expression"))
        
        res.register(self.advance())

        increment_expr = res.register(self.expr())
        if res.error: return res
        

        if self.current_tok.type != TT_RPAREN:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')"))
        res.register(self.advance())

        body_expr = res.register(self.boolExpr())
        return ForNode(var_name, stop_condition, increment_expr, body_expr)



    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None
        
        res.register(self.advance())
        if not self.current_tok.type == TT_LPAREN:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '('"))
        res.register(self.advance())
        condition = res.register(self.boolExpr())
        if res.error: return res
        if not self.current_tok.type == TT_RPAREN:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')'"))
        res.register(self.advance())
        expr = res.register(self.boolExpr())
        if res.error: return res
        cases.append((condition, expr))
        while self.current_tok.matches(TT_KEYWORD, 'elif'):
            res.register(self.advance())
            if not self.current_tok.type == TT_LPAREN:
                return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected '('"))
            res.register(self.advance())
            condition = res.register(self.boolExpr())
            if res.error: return res
            if not self.current_tok.type == TT_RPAREN:
                return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected ')'"))
            res.register(self.advance())
            expr = res.register(self.boolExpr())
            if res.error: return res
            cases.append((condition, expr))
        if self.current_tok.matches(TT_KEYWORD, "else"):
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res
            else_case = expr
        return res.success(IfNode(cases, else_case))
     

    def power(self):
        return self.bin_op(self.atom, (TT_POWER), self.factor)
    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))
        return self.power()

        

        
    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))
    def boolExpr(self):
        res = ParseResult()

        

        return self.bin_op(self.expr, [TT_COMPARE, TT_GREATERTHAN, TT_GREATERTHANEQ, TT_LESSTHAN, TT_LESSTHANEQ, TT_NOTEQUALTO, TT_NOT, TT_XOR, TT_AND, TT_OR])
    def expr(self):
        res = ParseResult()
       
       
        if self.current_tok.type == TT_INCREMENT:
            res.register(self.advance())
            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Identifier"))
            var_tok = self.current_tok
            res.register(self.advance())
            return res.success(VarIncrementNode(var_tok, 1)) 
        if self.current_tok.type == TT_CHAR:
            tok = self.current_tok
            res.register(self.advance())
            return res.success(CharNode(tok))
        if self.current_tok.type == TT_LITERAL:
            tok = self.current_tok
            res.register(self.advance())
            return res.success(StringNode(tok))  
        if self.current_tok.type == TT_IDENTIFIER:
            var_name = self.current_tok
            res.register(self.advance())
            if self.current_tok.type != TT_ASSIGNMENT:
                res.register(self.unadvance())
            else:
                res.register(self.advance())
                expr = res.register(self.expr())
                if res.error: return result
                return res.success(VarReassignNode(var_name, expr))
        if self.current_tok.matchesList(TT_TYPEKEYWORD, typeValues):
            var_type = self.current_tok
            res.register(self.advance())

                
            if(self.current_tok.type != TT_IDENTIFIER):
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,"Expected Identifier"))
            #identifier name or variable name
            var_name = self.current_tok
            res.register(self.advance())
            if self.current_tok.type != TT_ASSIGNMENT:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected assignment"))
            res.register(self.advance())
            if self.current_tok.type == TT_LITERAL and var_type.value != "string":
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, f"Expected type '{var_type.value}' got type 'string'"))
            expr = res.register(self.boolExpr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))



        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))


    def bin_op(self, func, ops, func_b=None):
        if(func_b == None):
            func_b = func
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func_b())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)
