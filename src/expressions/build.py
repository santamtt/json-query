from typing import Dict, List
from src.lexer import TokenType

def get_next(command: List) -> Dict:
    if len(command) == 0:
        return { "success": False, "message": "command not terminated"}
    return { "success": True, "token": command[0] }

def pick_token(command: List) -> Dict:
    if len(command) == 0:
        return { "success": False, "message": "command not terminated"}
    token_out: Dict = command.pop(0)
    return { "success": True, "token": token_out }

def check_token(command: List, control_type: TokenType, err_msg = "") -> Dict:
    option_token: Dict = pick_token(command)
    if not option_token["success"]:
        return option_token

    token_out: Dict = option_token["token"]
    if token_out["type"] != control_type:
        return { "success": False, "message": err_msg }
    return { "success": True, "token": token_out }

def check_types(command: List, types: List[TokenType]) -> Dict:
    result = { "success": False, "message": "expected one of the following types" }
    if len(command) == 0:
        result["message"] = "command not terminated" 
        return result

    token = command[0] 
    for token_type in types:
        if token["type"] == token_type:
            command.pop(0)
            result = { "success": True, "token": token }
            break

    return result

def primary(command: List[Dict], variables: Dict) -> Dict:
    option_primary = pick_token(command)
    if not option_primary["success"]:
        return option_primary
    token_primary = option_primary["token"]

    if token_primary["type"] == TokenType.OP_PAREN:
        option_expr = eq_expr(command, variables) 
        if not option_expr["success"]:
            return option_expr
        tmp_expr = option_expr["value"]

        is_closed = check_token(command, TokenType.CL_PAREN, "parenthesis not closed")
        if not is_closed["success"]:
            return is_closed
        return { "success": True, "value": tmp_expr }
    elif token_primary["type"] == TokenType.INT or token_primary["type"] == TokenType.FLOAT:
        return { "success": True, "value": token_primary["value"] }
    elif token_primary["type"] == TokenType.NEG:
        option_body = eq_expr(command, variables)
        if not option_body["success"]:
            return option_body
        return { "success": True, "op": TokenType.NEG, "value": option_body["value"] }
    elif token_primary["type"] == TokenType.ID:
        if not token_primary["name"] in variables.keys():
            return { "success": False, "message": f"used not declared variable '{token_primary["name"]}'" }
        return { "success": True, "value": variables[token_primary["name"]] }
    elif token_primary["type"] == TokenType.MINUS:
        option_primary = primary(command, variables)
        if not option_primary["success"]:
            return option_primary
        primary_expr = option_primary["value"]
        return { "success": True, "value": { "op": TokenType.MINUS, "value": primary_expr } }
    return { "success": False, "message": "malformed primary expression" }


def mult_expr(command: List[Dict], variables: Dict) -> Dict:
    option_left = primary(command, variables)
    if not option_left["success"]:
        return option_left
    left = option_left["value"]

    option_op = check_types(command, [TokenType.MULT, TokenType.DIV])
    if not option_op["success"]:
        return option_left
    token_op = option_op["token"] 
    
    option_right = primary(command, variables)
    if not option_right["success"]:
        return option_right
    right = option_right["value"]

    return { "success": True, "value": { "op": token_op, "left": left, "right": right } }


def add_expr(command: List[Dict], variables: Dict) -> Dict:
    option_left = mult_expr(command, variables)
    if not option_left["success"]:
        return option_left
    left = option_left["value"]

    option_op = check_types(command, [TokenType.PLUS, TokenType.MINUS])
    if not option_op["success"]:
        return option_left
    token_op = option_op["token"] 
    
    option_right = mult_expr(command, variables)
    if not option_right["success"]:
        return option_right
    right = option_right["value"]

    return { "success": True, "value": {"op": token_op, "left": left, "right": right }}

def eq_expr(command: List[Dict], variables: Dict) -> Dict:
    option_left = add_expr(command, variables)
    if not option_left["success"]:
        return option_left
    left = option_left["value"]

    option_op = check_types(command, [
        TokenType.DOUBLE_EQ, 
        TokenType.NEQ, 
        TokenType.GT, 
        TokenType.LT, 
        TokenType.GTE, 
        TokenType.LTE
    ])

    if not option_op["success"]:
        return option_left
    token_op = option_op["token"] 
    
    option_right = add_expr(command, variables)
    if not option_right["success"]:
        return option_right
    right = option_right["value"]

    return { "success": True, "value": { "op": token_op, "left": left, "right": right } }

def build_tree(command: List[Dict], variables: Dict) -> Dict:
    res: Dict = eq_expr(command, variables)
    return res 
