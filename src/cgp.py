# Python Standard Modules
import os
import sys
import argparse
import requests

try:
    # Import 3rd-party Modules/Libraries
    from github import Github
    import github
    import pygit2
    from dotenv import load_dotenv
    load_dotenv()

except ModuleNotFoundError:
    print("Required Modules Not Installed...")
    print("(Run): pip install -r requirements.txt")
    sys.exit(2)

GITHUB_BASE_URL = "https://github.com"
GITHUB_LICENSE_API = "https://api.github.com/licenses/"
GITHUB_GITIGNORE_API = "https://api.github.com/gitignore/templates/"


def main():
    """
    Create-Git-Project
    Main Function of the Program
    """

    # Parse Command Line Arguments 
    parser = argparse.ArgumentParser()
    parser.add_argument("repoName", help="Repository Name", type=str)
    parser.add_argument("-l", "--license", help="Initialize Repository with (X) License", type=str)
    parser.add_argument("-gi", "--gitignore", help="Initialize Repository with (X) gitignore template", type=str)
    parser.add_argument("-ra", "--repoAccess", default="public", help="Create a public or private repository. [DEFAULT: public]", type=str)
    args = parser.parse_args()

    # Creata a Github Instance
    g = Github(os.environ["access_token"])

    # Verify Authentication
    if not verifyAuthentication(g):
        print("(Authentication Failed): Please Verify your access token...")
        sys.exit(4)

    # Get User 
    user = g.get_user()
    # Create A Repo Under User - Private/Public
    repo = user.create_repo(args.repoName, private=True if args.repoAccess.lower() == "private" else False)

    # Generate README 
    repo.create_file("README.md", "Initial commit", f"# {args.repoName}\n")
    # Generate LICENSE
    licenseContent = generateLicense(repo, args.license)
    if type(licenseContent) == int:
        print(f"Invalid License Key : API returned with a status code of {licenseContent}")
        sys.exit(5)
    else:
        repo.create_file("LICENSE", "Added License", licenseContent)

    # Generate .gitignore
    gitignoreContent = generateGitignore(repo, args.gitignore)
    if type(gitignoreContent) == int:
        print(f"Invalid Gitignore Key : API returned with a status code of {gitignoreContent}")
        sys.exit(5)
    else:
        repo.create_file(".gitignore", "Added gitignore Template", gitignoreContent)
    
    # Clone Remote Repository
    print(f"https://github.com/{user.login}/{args.repoName}")

    pygit2.clone_repository(f"{GITHUB_BASE_URL}/{user.login}/{args.repoName}", ".")

    print("Github Repository Created/Initialized and Cloned Locally :)")

    
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


def generateLicense(repo, license):

    if not license:
        return None

    r = requests.get(GITHUB_LICENSE_API + license)
    if r.status_code != 200:
        return r.status_code
    
    return r.json()["body"]


def generateGitignore(repo, key):

    if not key:
        return None

    r = requests.get(GITHUB_GITIGNORE_API + key)
    if r.status_code != 200:
        return r.status_code

    return r.json()["source"]


if __name__ == "__main__":
    main()
