# model/users.py
from fastapi import Depends, HTTPException, APIRouter, Form, Path
from .db import get_db
import bcrypt
import logging

UserRouter = APIRouter(tags=["User"])

# CRUD operations


# users login 
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # Set logging level to INFO
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # Set logging level to INFO

@UserRouter.post("/users/login/", response_model=dict)
async def login_users(
    username: str = Form(...), 
    password: str = Form(...), 
    db=Depends(get_db)
):
    # Query the database to check if the username exists and the user is an admin
    query_check_user = """
    SELECT users.UserID, users.Password, adminprofile.FullName, adminprofile.Email, adminprofile.Alias, adminprofile.Age, adminprofile.Position, adminprofile.Address
    FROM users
    JOIN adminprofile ON users.UserID = adminprofile.UserID
    WHERE users.Username = %s AND users.UserType = 'Admin'
    """
    db[0].execute(query_check_user, (username,))
    admin_user = db[0].fetchone()

    if admin_user:
        userid, stored_password, fullname, email, alias, age, position, address = admin_user

        # Compare the plain text password with the stored password
        if password == stored_password:
            # If username and password are correct, return admin profile data
            return {"user_id": userid, "username": username, "full_name": fullname, "email": email, "alias": alias, "age": age, "position": position, "address": address}
    
    # If username or password is incorrect, raise an HTTPException
    raise HTTPException(status_code=401, detail="Incorrect username or password")




@UserRouter.get("/users/", response_model=list)
async def read_user(
    db=Depends(get_db)
):
    query = "SELECT userid, username, password, usertype, personalinfo FROM users"
    db[0].execute(query)
    users = [{"userid": users[0], "username": users[1],"password": users[2],"usertype": users[3],"personalinfo": users[4]} for users in db[0].fetchall()]
    return users

@UserRouter.get("/users/{userid}", response_model=dict)
async def read_user(
    userid: int, 
    db=Depends(get_db)
):
    query = "SELECT userid, username, password, usertype FROM users WHERE userid = %s"
    db[0].execute(query, (userid,))
    users = db[0].fetchone()
    if  users:
        return {"userid": users[0], "username":users[1],"password":users[2],"usertype":users[3],"personalinfo":users[4]}
    raise HTTPException(status_code=404, detail="User not found")

@UserRouter.post("/users/{userid}", response_model=dict)
async def create_user(
    userid: int = Path(...),
    username: str = Form(...),
    password: str = Form(...),
    usertype: str = Form(...),
    personalinfo: str = Form(...),
    db=Depends(get_db)
):
    # Hash the password using bcrypt
    hashed_password = hash_password(str(password))

    query = "INSERT INTO users (userid, username,password, usertype,personalinfo) VALUES (%s, %s, %s, %s, %s)"
    db[0].execute(query, (userid,username,hashed_password, usertype, personalinfo))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute(" SELECT MAX(userid)  FROM users")
    new_userid = db[0].fetchone()[0]
    db[1].commit()

    return {"id": new_userid, "userid": userid, "username": username, "password": password,"usertype":usertype,"personalinfo":personalinfo}

@UserRouter.put("/users/{userid}", response_model=dict)
async def update_user(
   
    userid: int = Path(...),
    username: str = Form(...),
    password: str = Form(...),
    usertype: str = Form(...),
    personalinfo: str = Form(...) ,
    db=Depends(get_db)
):
    # Hash the password using bcrypt


    # Update user information in the database 
    query = "UPDATE users SET userid = %s, username= %s, password = %s,usertype = %s,personalinfo = %s WHERE userid = %s"
    db[0].execute(query, (userid, username,password, usertype, personalinfo ))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "User updated successfully"}
    
    # If no rows were affected, user not found
    raise HTTPException(status_code=404, detail="User not found")

@UserRouter.delete("/users/{userid}", response_model=dict)
async def delete_user(
    userid: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_user = "SELECT userid FROM users WHERE userid = %s"
        db[0].execute(query_check_user, (userid,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Delete the user
        query_delete_user = "DELETE FROM users WHERE userid = %s"
        db[0].execute(query_delete_user, (userid,))
        db[1].commit()

        return {"message": "User deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()

# Password hashing function using bcrypt
def hash_password(password: str):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')  # Decode bytes to string for storage

@UserRouter.post("/users/login/", response_model=dict)
async def login_usersistrator(
   username: str = Form(...), 
    password: str = Form(...), 
    db=Depends(get_db)
):
    # Query the database to check if the username exists
    query_check_user = "SELECT password FROM users WHERE username = %s"
    db[0].execute(query_check_user, (username,))
    user = db[0].fetchone()

    if user:
        # Retrieve the stored password from the database
        stored_password = user[0]

        if password == stored_password:
            # If username and password are correct, print login successful
             return {"message": "Login successful"}
    
    # If username or password is incorrect, raise an HTTPException
    raise HTTPException(status_code=401, detail="Incorrect username or password")