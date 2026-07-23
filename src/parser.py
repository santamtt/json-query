from typing import List, Dict
from .lexer import TokenType
from .expression import pick_token, check_token, check_types
import json

variables: Dict = {} 

def eval_expr(command: List) -> Dict:
    return { "success": False, "message": "not implemented yet" }

def load_json(command: List) -> Dict:

    option_token = check_token(command, TokenType.STR, "passed bad arguments to load function")
    if not option_token["success"]:
        return option_token
    token = option_token["token"]

    try:
        load = None
        with open(token["value"], 'r') as input_json:
            load = json.load(input_json)
        return { "success": True, "value": load }
    except Exception as e:
        return { "success": False, "message": f"something went wrong during JSON loading: {e}" } 


def assign(command: List) -> Dict:
    result: Dict = { "success": True }
    
    option_id: Dict = check_token(command, TokenType.ID, f"expected ID, got another type instead")
    if not option_id["success"]:
        return option_id
    token_id: str = option_id["token"]

    option_eq: Dict = check_token(command, TokenType.EQ, "bad assegnation: no equal assignation symbol found")
    if not option_eq["success"]:
        return option_eq
    token_eq = option_eq["token"]    

    option_str: Dict = pick_token(command)
    if not option_str["success"]:
        return option_str
    check_next: Dict = option_str["token"]

    if check_next["type"] == TokenType.LOAD:
        parse = load_json(command)
        if parse["success"]:
            variables[token_id["name"]] = parse["value"]
        else:
            result = parse

    elif check_next["type"] == TokenType.INT or check_next["type"] == TokenType.FLOAT or check_next["type"] == TokenType.ID:
            result = eval_expr(command)
    else:
        result = { "success": False, "message": f"""bad assegnation: invalid 
                  element of type {check_next.TokenType}"""}

    return result 

def print_tokens(command: List) -> Dict:
    print(command)
    return { "success": True }

def parse_command(command: List) -> Dict:

    result: Dict = None
    first: Dict = command.pop(0)
    
    if first["type"] == TokenType.LET:
        result = assign(command)
    elif first["type"] == TokenType.TOKENIZE:
        result = print_tokens(command)
    else:
        result = eval_expr(command)
        if result["success"]:
            print(result["value"])

    return result
