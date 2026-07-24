from typing import List, Dict 
from enum import Enum

class TokenType:
    LET = 1
    EQ = 2
    NEQ = 3
    DOUBLE_EQ = 4
    ID = 5
    SELECT = 6
    QUIT = 7
    LOAD = 8
    COMMA = 9
    PLUS = 10
    MINUS = 11
    MULT = 12
    DIV = 13
    OP_PAREN = 14
    CL_PAREN = 15
    INT = 16
    FLOAT = 17
    NEG = 18
    STR = 19
    DOT = 20
    TOKENIZE = 21
    GT = 22
    LT = 23
    GTE = 24
    LTE = 25

keywords = {
    "let": { "type": TokenType.LET },
    "quit": { "type": TokenType.QUIT },
    "select": { "type": TokenType.SELECT },
    "load": { "type": TokenType.LOAD },
    "tokenize": { "type": TokenType.TOKENIZE }
}

symbols = {
    "!": { "type": TokenType.NEG },
    "=": { "type": TokenType.EQ },
    "!=": { "type": TokenType.NEQ },
    "==": { "type": TokenType.DOUBLE_EQ },
    ",": { "type": TokenType.COMMA },
    "+": { "type": TokenType.PLUS },
    "-": { "type": TokenType.MINUS },
    "*": { "type": TokenType.MULT },
    "/": { "type": TokenType.DIV },
    "(": { "type": TokenType.OP_PAREN }, 
    ")": { "type": TokenType.CL_PAREN },
    ".": { "type": TokenType.DOT },
    ">": { "type": TokenType.GT },
    "<": { "type": TokenType.LT },
    ">=": { "type": TokenType.GTE },
    "<=": { "type": TokenType.LTE },
}

def gen_token(command: str, index: int, out: Dict) -> int:

    begin_chr = command[index]

    if begin_chr == '=':
        next_index = index + 1
        next_chr = command[next_index] if next_index < len(command) else None
        if next_chr == '=':
            out.append(symbols["=="])
            next_index += 1
        else:
            out.append(symbols["="])
        return next_index
    elif begin_chr == '!':
        next_index = index+1
        next_chr = command[next_index] if next_index < len(command) else None
        if next_chr == '=':
            out.append(symbols["!="])
            next_index += 1
        else:
            out.append(symbols["!"])
        return next_index 
    elif begin_chr == '>':
        next_index = index + 1
        next_chr = command[next_index] if next_index < len(command) else None
        if next_chr == '=':
            out.append(symbols[">="])
            next_index += 1
        else:
            out.append(symbols[">"])
        return next_index
    elif begin_chr == '<':
        next_index = index + 1
        next_chr = command[next_index] if next_index < len(command) else None
        if next_chr == '=':
            out.append(symbols["<="])
            next_index += 1
        else:
            out.append(symbols["<"])
        return next_index
    elif begin_chr == '"':
        tmp = ""
        tmp_index = index+1
        closed = False

        while tmp_index < len(command):
            if command[tmp_index] == '"':
                closed = True
                break

            tmp += command[tmp_index]
            tmp_index += 1
        if not closed: 
            raise Exception("lexical error: string not closed")

        out.append({'value': tmp, 'type': TokenType.STR})
        return tmp_index+1
    elif begin_chr.isdigit():
        tmp = str(begin_chr)
        tmp_index = index+1
        token = None

        while tmp_index < len(command):
            char = command[tmp_index]
            if char.isalpha():
                raise ArithmeticError(f"lexical error: invalid number {tmp}")
            elif char == '.':
                if tmp_index + 1 < len(command):
                    if not command[tmp_index + 1].isdigit():
                        raise ArithmeticError(f"lexical error: invalid number {tmp}.{command[tmp_index+1]}")
                else:
                    raise ArithmeticError(f"lexical error: invalid number {tmp}.")
            elif not char.isdigit() and char != '.':
                break
            tmp += char
            tmp_index += 1

        if '.' in tmp:
            token = {'value': float(tmp), 'type': TokenType.FLOAT}
        else:
            token = {'value': int(tmp), 'type': TokenType.INT}
        out.append(token)
        return tmp_index

    elif begin_chr in symbols.keys():
        out.append(symbols[begin_chr])
        return index+1
    else: 
        tmp = str(begin_chr)
        tmp_index = index+1
        token = None

        while tmp_index < len(command):
            char = command[tmp_index]
            if not char.isalnum() and char != '-' and char != '_':
                break
            tmp += char
            tmp_index += 1
        
        if tmp in keywords.keys():
            token = keywords[tmp]
        else:
            token = {'name': tmp, 'type': TokenType.ID}

        out.append(token)
        return tmp_index

def tokenize(command: str) -> List:
    out = []
    index = 0

    while index < len(command):
        char = command[index]
        if char == ' ' or char == '\t':
           index += 1 
           continue
        index = gen_token(command, index, out)
        
    return out
