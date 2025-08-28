import sys

def main():
    print("Hello from spider!")
    if len(sys.argv) < 2:
        print("No website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("Too many arguments provided")
        sys.exit(1)
    if not sys.argv[1].startswith("https://") and not sys.argv[1].startswith("http://"):
        print("Website provided must start with either 'https://' or 'http://'. Please provide the full link.")
        sys.exit(1)
    print(f"Starting crawl of: {sys.argv[1]}")

if __name__ == "__main__":
    main()
