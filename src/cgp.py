import os
import sys

try:
    from github import Github
    import github
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
        sys.exit(3)


    
def verifyAuthentication(g):
    """
    Verifies Authentication to Github
    Param: Github object
    Return: Boolean
    """
    try:
        g.get_user().login
    except github.GithubException.BadCredentialsException:
        return False
    return True


if __name__ == "__main__":
    main()
