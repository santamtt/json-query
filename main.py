import sys
from typing import Dict
from src.lexer import tokenize 
from src.parser import parse_command 

def main():
    while(True):
        command = input("> ")
        if command == "quit":
            break

        tokens: List = tokenize(command)
        exec_res: Dict = parse_command(tokens)

        if not exec_res["success"]:
            print(f"[FAILED] {exec_res["message"]}", file=sys.stderr)

    print("Exiting from the CLI, goodbye!")

if __name__ == "__main__":
    main()
