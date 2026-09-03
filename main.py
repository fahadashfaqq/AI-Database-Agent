from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel

from database import init_db, get_connection
from agents import Agent

from ai_agents import run_agent
import secrets
import itsdangerous


app = FastAPI(
    title="AI Agent For Databases"
)

SERVER_SESSION_ID = secrets.token_urlsafe(32)


app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY")
)



init_db()



class ChatRequest(BaseModel):
    message: str


class LoginRequest(BaseModel):
    email: str


@app.post("/login")
async def login(login_data: LoginRequest, request: Request):

    email = login_data.email.strip().lower()

    connection = get_connection()
    data = connection.cursor()

    data.execute(
        """
        SELECT * FROM admins
        WHERE email = ?
        """,
        (email,)
    )

    admin = data.fetchone()

    data.close()
    connection.close()

    # If email does not exist
    if not admin:

        raise HTTPException(
            status_code=401,
            detail="This email is not authorized."
        )

    # Save logged-in email in session
    request.session["user_email"] = email

    # This identifies the current server run
    request.session["server_session_id"] = SERVER_SESSION_ID

    return {
        "message": "Login successful"
    }




@app.post("/logout")
async def logout(request: Request):

    request.session.clear()

    return {
        "message": "Logged out successfully"
    }




@app.get("/")
async def home(request: Request):

    user_email = request.session.get("user_email")

    session_server_id = request.session.get(
        "server_session_id"
    )

    # User is logged in only if the session belongs
    # to the current server run
    if (
        user_email
        and session_server_id == SERVER_SESSION_ID
    ):
        return FileResponse(
            "static/index.html"
        )

    # Old or invalid session
    request.session.clear()

    return FileResponse(
        "static/login.html"
    )






@app.post("/chat")
async def chat(
    request_data: ChatRequest,
    request: Request
):

        # Get login information from session
    user_email = request.session.get("user_email")

    session_server_id = request.session.get(
        "server_session_id"
    )

    # Check if session is valid for the current server run
    if (
        not user_email
        or session_server_id != SERVER_SESSION_ID
    ):

        request.session.clear()

        raise HTTPException(
            status_code=401,
            detail="You are not authorized."
        )

    # Check empty message
    if not request_data.message.strip():

        return {
            "response": "Please enter a message."
        }

    try:

        
        response = run_agent(
            request_data.message
        )

        return {
            "response": response
        }

    except Exception as e:

        print("Error:", e)

        return {
            "response": "Sorry, I was unable to process your request."
        }



app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)
