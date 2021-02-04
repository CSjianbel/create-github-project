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

except ModuleNotFoundError:
    print("Required Modules Not Installed...")
    print("(Run): pip install -r requirements.txt")
    sys.exit(2)

# Github API's
GITHUB_BASE_URL = "https://github.com"
GITHUB_LICENSE_API = "https://api.github.com/licenses"
GITHUB_GITIGNORE_API = "https://api.github.com/gitignore/templates"

# access token .env
ACCESS_TOKEN = "/home/jianbel/bin/create-github-project/.env"

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
    parser.add_argument("-gtk", "--get-template-keys", help="Get Template keys for [git, license] from github api", type=str)
    parser.add_argument("-ra", "--repoAccess", default="public", help="Create a public or private repository. [DEFAULT: public]", type=str)
    args = parser.parse_args()

    # If user wants to see template keys for license or gitignore templates from github api
    if args.get_template_keys:
        sys.exit(getTemplateKeys(args.get_template_keys))

    token = getToken()
    # Creata a Github Instance
    g = Github(token)

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
    elif licenseContent:
        repo.create_file("LICENSE", "Added License", licenseContent)

    # Generate .gitignore
    gitignoreContent = generateGitignore(repo, args.gitignore)
    if type(gitignoreContent) == int:
        print(f"Invalid Gitignore Key : API returned with a status code of {gitignoreContent}")
        sys.exit(5)
    elif gitignoreContent:
        repo.create_file(".gitignore", "Added gitignore Template", gitignoreContent)
    
    # Clone Remote Repository
    os.mkdir(args.repoName)
    try:
        pygit2.clone_repository(f"{GITHUB_BASE_URL}/{user.login}/{args.repoName}", args.repoName)
    except:
        print(f"Error in cloning Repository - Remote Repository successfuly created : https://github.com/{user.login}/{args.repoName}")
        os.rmdir(args.repoName)
        sys.exit(500)

    print(f"Repository Url: https://github.com/{user.login}/{args.repoName}")
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
        
        
def getTemplateKeys(k):
    """
    Prints out templates key for license or gitignore templates from github api
    Params: str
    Return: code
    """
    code = 0
    if k.lower() == "license":
        r = requests.get(GITHUB_LICENSE_API)
        if r.status_code != 200:
            code = 1
        
        print("Github LICENSE template keys: ")
        for item in r.json():
            print(item["key"])
    elif k.lower() == "git":
        r = requests.get(GITHUB_GITIGNORE_API)
        if r.status_code != 200:
            code = 1
        
        print("Github .gitignore template keys: ")
        for item in r.json():
            print(item)

    else:
        print("Invalid argument for --get-template-keys! : options [git, license]")
        code = 2

    return code


def generateLicense(repo, license):
    """
    Generate License Template throught github api
    param: Github Repo Object, str
    return: None | int | str
    """
    if not license:
        return None

    r = requests.get(f"{GITHUB_LICENSE_API}/{license}")
    if r.status_code != 200:
        return r.status_code
    
    return r.json()["body"]


def generateGitignore(repo, key):
    """
    Generate .gitignore Template throught github api
    param: Github Repo Object, str
    return: None | int | str
    """
    if not key:
        return None

    r = requests.get(f"{GITHUB_GITIGNORE_API}/{key}")
    if r.status_code != 200:
        return r.status_code

    return r.json()["source"]


def getToken():
    """
    Gets Personal Access Token on set .env PATH
    return: str
    """
    with open(ACCESS_TOKEN) as f:
        return f.read().strip("\n")


if __name__ == "__main__":
    main()
