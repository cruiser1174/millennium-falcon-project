# millennium-falcon-project
 
# Web Application
This project has been built using a python-Flask backend connected to a React frontend. It is hosted on a localhost and can be started in a few steps:

1. Open a terminal and activate the backend virtual environment by running the activate script - from the root directory run _flask_backend\backend_venv\Scripts\activate_
2. Navigate to the _react_frontend_ directory
3. Start the backend by running _npm run start-backend_
4. Open a new terminal and repeat steps 1 and 2
5. Start the frontend by running _npm start_

These should open the application in your web browser at localhost/3000.

# CLI file
The CLI executable file is located in the _flask_backend_ directory and is called _give-me-the-odds.py_. Instructions to run the programme are:
1. Open a terminal and navigate to the _flask_backend_ directory.
2. Run the file from the command line followed by the millennium falcon and empire json file paths respectfully as arguments. For example, on a VScode powershell terminal, you can run an example scenario by typing _python3 give-me-the-odds.py galaxies\millennium-falcon-1.json scenarios\empire-4.json_ which should print 100 to the terminal, signalling that there is a 100% chance of successfully reacing the destination planet in time.
