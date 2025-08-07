# Social Media App Backend

## Overview
This project is the backend for a social media application, built using FastAPI and Python. It provides core functionalities such as creating, retrieving, updating, and voting on posts. The API is designed for performance and scalability, enabling seamless integration with front-end applications.



## Features
- *Post Management:* Create, read, update, and delete posts.

- *Voting System:* Upvote or downvote posts to enhance user engagement.

- *User Authentication:* Secure authentication using JWT (JSON Web Tokens).

- *RESTful API:* Well-structured endpoints for front-end integration.


## Technologies Used
- *Python:* Programming language for the backend.



- *FastAPI:* High-performance web framework for building APIs.


- *PostgreSQL:* For Database Management.


- *SQLAlchemy:* To interact with Postgres Relational Database.



- *Pydantic:* Data validation and settings management.



- *JWT:* For secure user authentication.



- *Uvicorn:* ASGI server for running the FastAPI application.


## Installation

### Prerequisites

- Python (v3.8 or higher)

- pip (Python package manager)

- A database (configure PostgreSQL)


### Steps

#### 1. Clone the Repository
```bash
git clone https://github.com/Divyansh031/courseSellingApp.git
cd courseSellingApp
```
#### 2. Set Up a Virtual Environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables: Create a .env file in the root directory and add the necessary configuration
```bash
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_db_password
DATABASE_NAME=your_db_name
DATABASE_USERNAME=your_db_user
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### 5. Run the Application
```bash
uvicorn app.main:app --reload
```
#### The API will be available at ```http://localhost:8000```.*


## API Endpoints

### Posts:

```GET /posts```: Retrieve all posts.

```POST /posts```: Create a new post.

```GET /posts/{id}```: Retrieve a specific post by ID.

```PUT /posts/{id}```: Update a post.

```DELETE /posts/{id}```: Delete a post.

### Votes:

```POST /vote```: Upvote or downvote a post.

### Users:

```POST /users```: Register a new user.

```GET /users/{id}```: Get user by ID.

```POST /login```: Authenticate a user and return a JWT token.


## Project Structure:

- `main.py`: Entry point for the FastAPI application.

- `routers/`: Contains route handlers for posts, users, login and votes.

- `schemas.py`: Pydantic models for data validation.

- `database.py`: Database connection setup.

- `oauth2.py`: JWT authentication logic.

- `requirements.txt`: List of Python dependencies.


## Usage
- Ensure your database server is running.

- Run the application using the command above.

- Use tools like Postman or cURL to interact with the API.

- Refer to the /docs endpoint (e.g. `http://localhost:8000/docs`) for interactive API documentation provided by FastAPI.


## Author
Divyansh Sharma
