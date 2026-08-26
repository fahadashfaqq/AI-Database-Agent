from langchain_core.tools import tool
from database import get_connection

@tool
def create_user(
                name:str,
                email:str,
                phone:str = None,
                city: str = None
    ) -> str:

    """
    create a new user in the database.

    Args:
        name: Full name of the user.
        email: Email address of the user.
        phone: Phone number of the user.
        city:city of the user.

    """


    conn = get_connection()
    data = conn.cursor()

    try:
        data.execute("SELECT id FROM users WHERE email = ?",(email,))

        existing_user=data.fetchone()

        if existing_user:
            return f"A user with email{email} already exists."

        data.execute(""" INSERT INTO users(name, email, phone, city) VALUES(?,?,?,?)""",(name, email, phone, city))

        conn.commit()

        return f"User{name} was created successfully."
    except Exception as e:
        return f"Error creating user:{str(e)}"
    finally:
        data.close()
        conn.close()


@tool
def search_user(
    
    name: str =None,
    email: str = None,
    phone: str = None,
    city: str = None,
    show_all: bool = False
    ) -> str:
    """
    Search for a user using their name or email.
    Args:
        name: Name of the user.
        email: Email address of the user.
        phone: Phone number of the user.
        city:city of the user.

        Set show_all=True only when the user explicitly asks
        to show all users or every user in the database.

        If no search information is provided and show_all is False,
        do not return any users.
    """

    conn = get_connection()
    data = conn.cursor()
    
    try:
        if show_all:

            data.execute(
                """
                SELECT id, name, email, phone, city
                FROM users
                """
            )

        elif email:
            data.execute("""SELECT id, name, email, phone, city FROM users WHERE email = ?""",(email,))
        elif name:
            data.execute("""SELECT id, name, email, phone, city FROM users WHERE name LIKE ?""",(f"%{name}%",))
        elif phone:
            data.execute("""SELECT id, name, email, phone, city FROM users WHERE phone LIKE ?""",(f"%{phone}%",))
        elif city:
            data.execute("""SELECT id, name, email, phone, city FROM users WHERE city LIKE ?""",(f"%{city}%",))
        else:
            return "Please provide a name or email to search."

        users = data.fetchall()

        if not users: 
            return "no users found"

        result = []

        for user in users:
            result.append({
                 "id":user[0],
                 "name":user[1],
                 "email":user[2],
                 "phone":user[3],
                    "city":user[4]  
                 })
        return str(result)

    except Exception as e:
        return f"Error searching user:{str(e)}"
    finally:
        data.close()
        conn.close()


@tool
def update_user(
    current_name: str = None,
    current_email: str = None,
    current_phone: str = None,
    current_city: str = None,
    name: str =None,
    email: str = None,
    phone: str = None,
    city: str = None
    ) -> str:
    """
    Update one or more fields of an existing user.
    Args:
       
        Use current_name or current_email or current_phone or current_city to find the existing user.
        Then provide any new values for name, email, phone, or city.
    """

    conn = get_connection()
    data = conn.cursor()
    
    try:
          
        if not current_name and not current_email and not current_phone and not current_city:
            return "Please provide the user's current name or current email to identify the user."

        
        if current_email:

            data.execute(
                "SELECT * FROM users WHERE email = ?",
                (current_email,)
            )

        elif current_name:

            data.execute(
                "SELECT * FROM users WHERE name = ?",
                (current_name,)
            )

        elif current_phone:
        
            data.execute(
                "SELECT * FROM users WHERE phone = ?",
                (current_phone,)
            )

        elif current_city:
        
            data.execute(
                "SELECT * FROM users WHERE city = ?",
                (current_city,)
            )

        users = data.fetchone()

        if not users: 
            return f"Users was not found."

        fields = []
        values = []

        
        if name is not None:
            fields.append("name=?")
            values.append(name)

        if email is not None:
            fields.append("email=?")
            values.append(email)
        
        if phone is not None:
            fields.append("phone=?")
            values.append(phone)

        if city is not None:
            fields.append("city=?")
            values.append(city)
        
        if not fields:
            return "No information was provided to update."

        values.append(users["id"])

        query=f"""UPDATE users SET {", ".join(fields)} WHERE id=?"""

        data.execute(query, values)
        conn.commit()

        return f"User updated successfully"

    except Exception as e:
        return f"Error updating user:{str(e)}"
    finally:
        data.close()
        conn.close()


@tool
def delete_user(
    current_name: str = None,
    current_email: str = None,
    current_phone: str = None,
    current_city: str = None
) -> str:
    """
    Delete a user using one or more identifying details.

    You can use:
    - current_name
    - current_email
    - current_phone
    - current_city

    Multiple details can be provided together to identify
    the correct user more precisely.
    """

    conn = get_connection()
    data = conn.cursor()

    try:

        
        if not any([
            current_name,
            current_email,
            current_phone,
            current_city
        ]):
            return "Please provide at least one detail to identify the user."

        
        conditions = []
        values = []

        if current_name:
            conditions.append("name = ?")
            values.append(current_name)

        if current_email:
            conditions.append("email = ?")
            values.append(current_email)

        if current_phone:
            conditions.append("phone = ?")
            values.append(current_phone)

        if current_city:
            conditions.append("city = ?")
            values.append(current_city)

       
        query = f"""
            SELECT * FROM users
            WHERE {" AND ".join(conditions)}
        """

        data.execute(query, values)

        users = data.fetchall()

        
        if not users:
            return "No user was found with the provided information."

       
        if len(users) > 1:
            return (
                "Multiple users were found. "
                "Please provide more information to identify the correct user."
            )

        
        user = users[0]

        user_id = user["id"]
        user_name = user["name"]

        
        data.execute(
            "DELETE FROM users WHERE id = ?",
            (user_id,)
        )

        conn.commit()

        return f"User {user_name} was deleted successfully."

    except Exception as e:

        return f"Error deleting user: {str(e)}"

    finally:

        data.close()
        conn.close()

tools = [
    
    create_user,
    search_user,
    update_user,
    delete_user
    
    ]

