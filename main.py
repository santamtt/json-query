from src.lexer import *

def main():
    while(True):
        command = input("> ")
        tokens = tokenize(command)
        print(tokens)
        if command == "quit":
            break
    print("Exiting from the CLI, goodbye!")

if __name__ == "__main__":
    main()
