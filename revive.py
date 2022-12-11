import sys
from core.prompt import Terminal


if __name__ == "__main__":
    try:
        Terminal()
    except KeyboardInterrupt:
        sys.exit(0)
