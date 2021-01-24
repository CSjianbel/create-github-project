import os
import sys

try:
    from github import Github
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    print("Required Modules Not Installed...")
    print("Run: pip install -r requirements.txt")
    sys.exit(2)

if len(sys.argv) not in list(range(3, 6)):
    print("Usage: create-git-project [repository name] --license [license*] --repo-access [repository access*]")
    sys.exit(1)

def main():
    print(os.environ["access_token"])

    g = Github(os.environ["access_token"])

    # Verify Authentication
    if not verifyAuthentication(g):
        print("Authentication Failed Verify your access token...")


    # Then play with your Github objects:
    for repo in g.get_user().get_repos():
        print(repo.name)
    
def verifyAuthentication(g):

    # ff36637c46f3415b6753bf950d5c9df9ca24d63b

    try:
        g.get_user().get_repos()
    except:
        return False

    return True


if __name__ == "__main__":
    main()
