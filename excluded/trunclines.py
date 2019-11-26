import sys
import re

if __name__ == '__main__':
    fi = sys.argv[1]
    lines = []
    with open(fi) as f:
        lines = ''.join(f.readlines())
    with open(fi, mode='w') as f:
        f.write(re.sub(r'\n\n\n+', '\n\n', lines))
