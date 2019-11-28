import sys
import re

def fixLatex(line):
    return re.sub(r"(?<!\$)\$(.+?)\$(?!\$)", r"\n$$\1$$\n", line)

if __name__ == '__main__':
    fi = sys.argv[1]
    lines = []
    with open(fi) as f:
        lines = ''.join(fixLatex(line) for line in f.readlines())
    with open(fi, mode='w') as f:
        f.write(re.sub(r'\n\n\n+', '\n\n', lines))
