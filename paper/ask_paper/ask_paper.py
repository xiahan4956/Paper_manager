import os
import sys
sys.path.append(os.getcwd())
from utils.claude import *


def load_paper():
    with open(r"paper/ask_paper/paper.txt", "r", encoding="utf-8") as f:
        paper = f.read()
    return paper

def ask_paper_run():
    paper = ""
    
    while True:
        print(f"Please input a question:")
        question = input()
        paper = load_paper()
        pmt = paper + "\n" + question
        print("....")
        ask_claude(pmt)


if __name__ == "__main__":
    ask_paper_run()