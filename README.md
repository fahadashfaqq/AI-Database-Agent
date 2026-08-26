# AI Database Management Agent

This project was developed as part of a technical assessment.

It is an AI-powered application that allows an administrator to manage user information through natural language commands.

## Features

- Email-based admin authentication
- Add users
- Search users
- Update user information
- Delete users
- View all users
- Natural language interaction through an AI agent
- SQLite database
- Chat-style user interface

## Technologies Used

- Python
- FastAPI
- SQLite
- LangGraph
- LangChain
- OpenAI API
- HTML
- CSS
- JavaScript

## Setup

1. Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL

2. Move into the project folder:

cd AI-Database-Management-Agent

3. Create a virtual environment:
python -m venv venv

4. Activate the virtual environment

venv\Scripts\activate

5. Install dependencies:
python -m pip install -r requirements.txt

6. Create a .env file and add your OpenAI API key:
OPENAI_API_KEY=your_api_key_here

7. Run the application:
uvicorn main:app --reload

8. Open the application:
http://127.0.0.1:8000

9. Login Email
admin@example.com


## Example Commands

The administrator can use commands such as:

```text
Add a user named Jane with email Jane@example.com,
phone +91253 and city New York.

Find the user with email fahad@example.com

Update Fahad's city to Lahore.

Delete the user Fahad.

Show all users.



1. Authentication

The application uses email-based authentication.

Only email addresses that exist in the admins table are allowed to access the application.

The application also uses session-based authentication to protect the chat functionality.


2. Database Operations

The AI agent can perform the following operations:

Create User

Add a new user with:

Name
Email
Phone
City
Search User


Search for users using:

Name
Email
Phone number
City
Update User


Update one or more user fields without manually providing a database ID.

Delete User

Delete a user using available information such as:

Name
Email
Phone number
City
Show All Users

Display all users stored in the database.