# Mathpuzzle server (API)

## Dependencies
Make and activate virtual environment.

To install all dependencies, run
```
$ pip install -r requirements.txt
```
If you have added some dependencies, run
```
$ pip freeze > requirements.txt
```

## Secret key
To specify secret key, create `.env` file with `SECRET_KEY` variable:
```
SECRET_KEY="<your secret key>"
```
