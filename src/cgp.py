# Python Standard Modules
import os
import sys
import argparse

try:
    # Import 3rd-party Modules/Libraries
    from github import Github
    import github
    from dotenv import load_dotenv
    load_dotenv()

except ModuleNotFoundError:
    print("Required Modules Not Installed...")
    print("(Run): pip install -r requirements.txt")
    sys.exit(2)


def main():
    """
    Create-Git-Project
    Main Function of the Program
    """

    # Parse Command Line Arguments 
    parser = argparse.ArgumentParser()
    parser.add_argument("repoName", help="Repository Name", type=str)
    parser.add_argument("-l", "--license", help="Initialize Repository with (X) License", type=str)
    parser.add_argument("-ra", "--repoAccess", help="Create a public or private repository. [DEFAULT: public]", type=str)
    args = parser.parse_args()
    print(args)

    # Creata a Github Instance
    g = Github(os.environ["access_token"])

    # Verify Authentication
    if not verifyAuthentication(g):
        print("(Authentication Failed): Please Verify your access token...")
        sys.exit(3)

    # Get User 
    user = g.get_user()
    # Create A Repo Under User - Private/Public
    repo = user.create_repo(args.repoName, private=True if args.repoAccess.lower() == "private" else False)

    
def verifyAuthentication(g):
    """
    Verifies Authentication to Github
    Param: Github object
    Return: Boolean
    """
    try:
        g.get_user().login
    except github.GithubException:
        return False
    return True


if __name__ == "__main__":
    main()
