# Reconciler

Tool that reconciles data from two csv files

!["Reconciler gif"](reconciler.gif)

### Tech

- Python
- Pandas
- Django

### Running the app

1. Clone the project at https://github.com/the-krafty-koder/reconciliation
2. Launch your terminal and navigate to the project's root folder.
3. Optional: create and launch a virtual environment. The command may vary depending on your OS
   > virtualenv venv
4. Optional: activate the virtual environment if it was created
   > source venv/bin/activate
5. Run the following commands on the terminal, one after the other
   > pip install -r requirements.txt
   > ./manage.py migrate
   > ./manage.py runserver
6. Navigate to your browser at localhost:8000 and upload files to use the reconciliation tool
