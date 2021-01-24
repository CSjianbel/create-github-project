from sys import argv

if len(argv) not in list(range(3, 6)):
    print("Usage: create-git-project [author] [repository name] [license*] [repository access]")
    sys.exit(1)

