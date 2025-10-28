# Social Media App Backend

## Overview
This project is the backend for a social media application, built using FastAPI and Python. It provides core functionalities such as creating, retrieving, updating, and voting on posts. The API is designed for performance and scalability, enabling seamless integration with front-end applications.

---

## 🌐 Project Architecture: The 3-Tier Model

This project is deployed using the **3-Tier Web Architecture** pattern, a highly common and scalable structure that separates the application into three logical and physical layers. This modularity allows for easier maintenance, scaling, and security.

### 🧱 The Typical 3-Tier Structure and Its Problems

A typical web application is conceptually divided into three tiers:

| Tier | Component | Role | Potential Problems in Traditional Setup |
| :--- | :--- | :--- | :--- |
| **Presentation (Client)** | Web Browser, Mobile App | How the user interacts. | N/A |
| **Application (Logic)** | Your FastAPI App | Processes requests, runs business logic. | **Single Point of Failure:** If the server fails, the entire application goes down. |
| **Data (Storage)** | PostgreSQL Database | Stores all application data. | **Security Risk:** Direct exposure of the database to the application server increases the attack surface. |

In a traditional setup, the **Application Tier** (FastAPI) might directly expose ports to the internet, and scaling involves complex load balancer setups.

### 🐳 Our Solution: Containerized Architecture

We solve the problems of the traditional setup by utilizing **Docker and Docker Compose** to containerize and orchestrate the tiers, adding a powerful Nginx reverse proxy layer.

| Tier | Component (Docker Service) | Role and Solution |
| :--- | :--- | :--- |
| **Presentation (Client)** | User's Browser (You) | The client makes a request to the single entry point. |
| **Reverse Proxy (Entry)** | **Nginx** container | The **only public-facing component** (Port 80). It provides high performance, load balancing, and hides the application container's port, enhancing **security**. |
| **Application (Logic)** | **Python App** container | Runs the FastAPI application on its private network port (8000). It receives requests forwarded by Nginx, executes the business logic, and connects to the Data Tier. |
| **Data (Storage)** | **PostgreSQL (DB)** container | Stores data. It is only accessible by the Application container on the internal Docker network, ensuring maximum **security isolation**. |

### ♻️ **Request Flow (As a Developer hitting Nginx)**

1.  **Client $\rightarrow$ Nginx:** Your browser hits the public entry point: `http://localhost`.
2.  **Nginx $\rightarrow$ Python App:** Nginx receives the request, forwards it to the Python App service (e.g., `http://backend:8000`).
3.  **Python App $\rightarrow$ DB:** The Python App processes the request and connects to the DB service (e.g., `db:5432`) to fetch or save data.
4.  **DB $\rightarrow$ Python App:** The DB sends the result set back to the Python App.
5.  **Python App $\rightarrow$ Nginx:** The Python App constructs the final response and sends it back to Nginx.
6.  **Nginx $\rightarrow$ Client:** Nginx sends the final response back to your browser.

---

## 🔗 Features
* **Post Management:** Create, read, update, and delete posts.
* **Voting System:** Upvote or downvote posts to enhance user engagement.
* **User Authentication:** Secure authentication using JWT (JSON Web Tokens).
* **RESTful API:** Well-structured endpoints for front-end integration.

---

## 🛠️ Technologies Used
* **Python:** Programming language for the backend.
* **FastAPI:** High-performance web framework for building APIs.
* **PostgreSQL:** For Database Management.
* **SQLAlchemy:** To interact with Postgres Relational Database.
* **Pydantic:** Data validation and settings management.
* **JWT:** For secure user authentication.
* **Uvicorn:** ASGI server for running the FastAPI application.
* **Docker/Docker Compose:** For containerization and orchestration of all 3-tiers.
* **Nginx:** High-performance reverse proxy and web server.

--- 

# ⬇️ Installation(Using Docker)
### Prerequisites

* **Docker Desktop** (or Docker Engine) installed and running.
---

### Steps

### 1. Clone the Repository
```bash
git clone https://github.com/Divyansh031/social-media-app-with-nginx.git 
cd social-media-app-with-nginx
```
### 2. Environment Configuration

**We do use a local `.env` file**. All necessary environment variables (Database credentials, Secret Key, etc.) are securely configured directly within the `docker-compose.yml` using `.env` file for the `backend service`, allowing the containers to manage their own settings.

### 3. Start the Services
Build the images and start the application:
```bash
docker-compose up --build -d
```
*The `-d` flag runs the containers in detached mode.*

### 4. Access the API
The **Nginx** container is now listening on port 80.
- The API endpoints will be available at: http://localhost

- Interactive documentation (Swagger UI) is available at: http://localhost/docs

---

# ⬇️ Installation(Traditionally)

### Prerequisites

- Python (v3.8 or higher)

- pip (Python package manager)

- A database (configure PostgreSQL)
---

### Steps

#### 1. Clone the Repository
```bash
git clone https://github.com/Divyansh031/social-media-app-with-nginx.git 
cd social-media-app-with-nginx
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


## 🔗 API Endpoints

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


## 🧱 Project Structure:

- `main.py`: Entry point for the FastAPI application.

- `routers/`: Contains route handlers for posts, users, login and votes.

- `schemas.py`: Pydantic models for data validation.

- `database.py`: Database connection setup.

- `oauth2.py`: JWT authentication logic.

- `requirements.txt`: List of Python dependencies.

- `tests/`: Testing functionalities using pytest.

- `Dockerfile`: Defines the build environment for the Python App container.

- `docker-compose.yml`: Defines and orchestrates the 3-tier services (Nginx, Python App, DB).

- `nginx.conf`: Custom configuration for the Nginx reverse proxy.

## 📢 Usage
- If using Docker Setup, ensure all Docker services are running (`docker-compose ps`)

- Ensure your database server is running.

- Run the application using the commands above.

- Use tools like Postman or cURL to interact with the API.

- Refer to the /docs endpoint for interactive API documentation provided by FastAPI.


## 🧪 Testing
This project includes unit and integration tests implemented using pytest to ensure the reliability of the backend functionalities.

### Running Tests
1. Install pytest if not already included in your dependencies
```bash
pip install pytest
```

2. Run the tests from `tests` directory
```bash
pytest tests -v -s
```

*This will discover and execute all test files (typically in a tests/ directory or named with test_ prefix).*

**Note: Ensure your test environment is set up, such as using a test database configuration in your .env file or via environment variables to avoid affecting production data.**

## 👤 Author
Divyansh Sharma
