from typing import List, Dict
from .lexer import TokenType
from .expression import get_next, pick_token, check_token, build_tree 
import json

variables: Dict = {} 

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

    option_str: Dict = get_next(command)
    if not option_str["success"]:
        return option_str
    check_next: Dict = option_str["token"]

    if check_next["type"] == TokenType.LOAD:
        parse = load_json(command)
        if parse["success"]:
            variables[token_id["name"]] = parse["value"]
        else:
            result = parse
    else:
        option_tree = build_tree(command, variables)
        if option_tree["success"]:
            variables[token_id["name"]] = 0 
        result = option_tree

    return result 

def print_tokens(command: List) -> Dict:
    print(command)
    return { "success": True }

def parse_command(command: List) -> Dict:

    result: Dict = None
    first: Dict = command[0]
    
    if first["type"] == TokenType.LET:
        command.pop(0)
        result = assign(command)
    elif first["type"] == TokenType.TOKENIZE:
        command.pop(0)
        result = print_tokens(command)
    else:
        result = build_tree(command, variables)

    return result
