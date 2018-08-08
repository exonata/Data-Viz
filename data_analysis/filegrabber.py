import sys
import glob


def main():
    dirname = sys.argv[1]
    filepath = dirname + '/*'
    print(filepath)
    for name in glob.glob(filepath):
        print(name)


if __name__ == '__main__':
   main()