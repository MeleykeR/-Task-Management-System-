# How to install and run locally

1. run `pip install -r requirements.txt`
2. run `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
3. navigate to `http://127.0.0.1:8000/docs` and check out documentation
4. execute /populate_dummy_data api endpoint to populate dummy data or /reset_database endpoint to reset the database and remove all data

# How to deploy

1. Use online platforms like https://render.com to deploy the project.
1. Use `pip install -r requirements.txt` as build command.
1. Use `uvicorn main:app --host 0.0.0.0 --port 80` as start command.


