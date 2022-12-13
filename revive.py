import sys
import argparse
from core.settings import Server
from core.prompt import Terminal

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', action='store',
                    help="To load presistant result file (*.result/*.sqlite3)",
                    dest="file")
args = parser.parse_args()
if args.file:
    Server.storage = args.file


if __name__ == "__main__":
    try:
        Terminal()
    except KeyboardInterrupt:
        sys.exit(0)
