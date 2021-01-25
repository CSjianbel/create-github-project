# Create Github Project

Initialize a Github Repository.<br />
Options to initialize Repository with a **LICENSE** and **.gitignore** templates.<br />

## Clone

```bash
git clone "https://github.com/CSjianbel/create-github-project.git"
```

## Compilation

```bash
cd create-github-project

pip install -r requirements.txt

cd src

pyinstaller --onefile cgp.py
```

## Setup

Ideally the compiled executable must be added onto your PATH.<br />
Therefore you will have access to the executable globally in your system.<br />

### Linux Setup

- Create a **bin/** directory in your root directory (~)
- Create another directory within the bin directory
- Create a personal acceess token on github, and create a **.env** file
- Add your token inside your **.env**
- Go to the cloned git repo then modify **src/cgp.py**
- Look for **ACCESS\_TOKEN** variable and modify it to your desired path to the **.env** file that contains the token
- Follow the **Compilation** steps
- Move the compiled executable made by **PyInstaller** to the directory made in **~/bin/**
- Add the directory of the executable to your **PATH**

## Usage

```bash
cgp.py [-h] [-l LICENSE] [-gi GITIGNORE] [-ra REPOACCESS] repoName
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### License

[MIT](https://choosealicense.com/licenses/mit/)

_A Project by Jiankarlo A. Belarmino_
