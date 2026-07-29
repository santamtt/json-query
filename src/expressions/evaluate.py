from src.lexer import TokenType
from numbers import Number
from typing import Dict, List 

def eval_tree(option_expr: Dict) -> Dict:
    if option_expr["is_primary"]:
        return option_expr 
    expression = option_expr["value"] 

    left = None
    ignore_left = True
    if expression["left"] is not None:
        option_left = eval_tree(expression["left"])
        if not option_left["success"]:
            return option_left 
        left = option_left["value"]
        ignore_left = False

    option_right = eval_tree(expression["right"])
    if not option_right["success"]:
        return option_right 
    right = option_right["value"]

    op: TokenType = expression["op"]
    if op == TokenType.PLUS:
        return { "success": True, "value" : left + right }
    elif op == TokenType.MINUS:
        if ignore_left:
            left = 0 
        return { "success": True, "value": left - right }
    elif op == TokenType.MULT:
        return { "success": True, "value": left * right }
    elif op == TokenType.DIV:
        return { "success": True, "value": left / right  }
    elif op == TokenType.GT:
        return { "success": True, "value": left > right  }
    elif op == TokenType.LT:
        return { "success": True, "value": left < right }
    elif op == TokenType.GTE:
        return { "success": True, "value": left >= right }
    elif op == TokenType.LTE:
        return { "success": True, "value": left <= right }
    elif op == TokenType.DOUBLE_EQ:
        return { "success": True, "value": left == right }
    elif op == TokenType.NEQ:
        return { "success": True, "value": left != right }
    elif op == TokenType.NEG:
        return { "success": True, "value": not right }
    elif op == TokenType.AND:
        return { "success": True, "value": left and right }
    elif op == TokenType.OR:
        return { "success": True, "value": left or right }
    else:
        return { "success": False, "message": "unrecognized expression" }
