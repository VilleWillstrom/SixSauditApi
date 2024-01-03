# SixSauditApi

SixSauditApi is the backend for a 6S auditing app, developed in Python using the FastAPI framework. While the project is currently under development, it is fully runnable for demonstration purposes.

## Getting Started

To run this program, you'll need Xampp or an equivalent method to host a MySQL database.

The software leverages the FastAPI framework and integrates SQLAlchemy to connect to the database. This simplifies the setup process as you only need to initialize a fresh database, and SQLAlchemy will handle the rest during the initial usage.

### Prerequisites

Make sure you have the following prerequisites installed:

- [Xampp](https://www.apachefriends.org/index.html) or equivalent
- [Python](https://www.python.org/downloads/) (version X.X.X)
- [pip](https://pip.pypa.io/en/stable/installation/)

## Installation Steps

### 1. Open the Project Folder:

- Open the project folder in the editor of your choice.

### 2. Create a `.env` File:

- Create a new file in the project root and name it `.env`.
- Copy the lines from `.envexample` and paste them into `.env`.
- Provide a random string for `JWT_SECRET` in `.env`.
- Add the direct path to your fresh database to `CONNECTION_STRING` in `.env` after the `mysql+mysqlconnector://` text.

### 3. Install Packages:

- Ensure you are in a virtual environment.
- Open the command prompt and navigate to the root of this project.
- Run the command `pip install -r requirements.txt`.
  This installs the required packages from `requirements.txt`, ensuring you have all the necessary dependencies.

### 4. Create a Static Folder:

- Create a new folder in the project root and name it `static`.
  This folder is where the API stores all static files uploaded to the server.

### 5. Create SSL HTTPS for Localhost:

- Follow [this tutorial](https://www.section.io/engineering-education/how-to-get-ssl-https-for-localhost/) to create the `cert` folder in the project root and continue with the tutorial to provision an SSL certificate for the local server.

### 6. Run Alembic Upgrade Head Command:

- Navigate to the project root directory using the command prompt and execute the following command:
`alembic upgrade head` This command initializes the database by applying any pending migrations, creating the necessary tables on your fresh database.

- Ensure the database is properly set up before proceeding to the next steps.

### 7. Run the Program:

- Ensure you are at the project root.
- Run the command `python main.py`.
- Open the app from the link shown in the terminal.
- Navigate to the `/docs` page (e.g., `localhost:8002/docs`).
  You should now see the API documentation.

## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.

---

**MIT License**

Copyright (c) 2024 Ville Willström

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
