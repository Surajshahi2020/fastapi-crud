from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserResponse
from database import SessionLocal, engine, Base

# Create the database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="My Custom API Title",        # Title of the Swagger UI
    description="This is a custom API for managing users.",  # Description of the API
    version="1.0.0",                    # Version of the API
    docs_url="/documentation",          # URL for the Swagger docs (default is "/docs")
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new user
@app.post("/users/", response_model=UserResponse, tags=["User Operations"], summary="Create a new user", description="This endpoint allows you to create a new user with name, email, and password.")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create a new user instance
    db_user = User(name=user.name, email=user.email, password=user.password)
    
    # Add the new user to the database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# Get all users
@app.get("/users/", response_model=list[UserResponse], tags=["User Operations"], summary="Get all the list of the user", description="This endpoint allows you to list all user with information id, name, email, and password.")
def get_users(db: Session = Depends(get_db)):
    # Query the database to get all users
    users = db.query(User).all()
    return users

# Update an existing user (PUT)
@app.put("/users/{user_id}", response_model=UserResponse, tags=["User Operations"], summary="Update the existing user", description="This endpoint allows you to update the existing user with name, email, and password.")
def update_user(user_id: int, user_update: UserCreate, db: Session = Depends(get_db)):
    # Find the user in the database
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update fields if provided in the request
    if user_update.name:
        db_user.name = user_update.name
    if user_update.email:
        db_user.email = user_update.email
    if user_update.password:
        db_user.password = user_update.password
    
    # Commit changes to the database
    db.commit()
    db.refresh(db_user)
    
    return db_user

# Delete a user (DELETE)
@app.delete("/users/{user_id}", response_model=UserResponse, tags=["User Operations"], summary="Delete the existing user", description="This endpoint allows you to delete a existing user with name, email, and password.")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # Find the user in the database
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete the user from the database
    db.delete(db_user)
    db.commit()
    
    return db_user