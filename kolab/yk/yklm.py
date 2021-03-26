

def conv(file):
    with open(file) as f:
        for line in f.readlines():
            line = line.strip()
            if "。" in line: 
                print(line)

if __name__ == '__main__':
    import sys
    for file in sys.argv[1:]:
        conv(file)
