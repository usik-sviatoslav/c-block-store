# **C-BLOCK-STORE**

**C-BLOCK-STORE** is a project that integrates Django and FastAPI to store and
retrieve the latest blocks for BTC and ETH using external APIs.
The application allows for efficient data retrieval and
management while leveraging Django's ORM and FastAPI's speed.

## Features
- **Hybrid Django & FastAPI application** with seamless integration.
- **Django Admin** for easy database management.
- **FastAPI for API endpoints** providing high-speed access.
- **Asynchronous tasks** to fetch the latest blocks every minute.
- **User authentication** with account creation and login.
- **Filtering and pagination** for block retrieval.

## Project Structure
```plaintext
c-block-store/
│── src/
│   ├── api/                  # FastAPI layer: CRUD, dependencies, routes, schemas, and utilities
│   │   ├── crud/             # Database operations
│   │   ├── dependencies/     # FastAPI dependencies
│   │   ├── routes/           # FastAPI routes
│   │   ├── schemas/          # Pydantic schemas
│   │   └── utils/            # Helper functions
│   ├── apps/                 # Django applications
│   │   ├── block/            # Business logic for blocks
│   │   │   └── handlers/     # Event handlers
│   │   ├── currency/         # Business logic for currencies
│   │   ├── provider/         # Business logic for providers
│   │   └── user/             # Authentication and user management
│   ├── core/                 # Main project settings
│   │   ├── config/           # Project configuration
│   │   ├── django/           # Django settings and utilities
│   │   └── fastapi/          # FastAPI settings
│   ├── scripts/              # Automation scripts
│   └── static/               # Static files
```
---

## Installation & Setup
### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Poetry (for dependency management)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/usik-sviatoslav/c-block-store.git
   cd c-block-store
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Create a `.env` file based on `.env.example` and set up environment variables.

4. Build and start the containers:
   ```bash
   make build
   make up
   ```
   If you don't have installed `Make`, use the following command:
   ```bash
   docker build --build-arg ENV_STATE=production --target base -t c-block-store:latest .
   docker compose up -d
   ```
---

## Background Tasks
The application includes a scheduled task that fetches the
latest BTC and ETH blocks every minute and saves them in the database.

### How it works:
1. **Creating a superuser:** To create a superuser, run the command:
   ```bash
   make create-superuser
   ```
   If you don't have installed `Make`, use the following command:
   ```bash
   docker compose up -d
   docker exec -it backend python manage.py createsuperuser
   ```
   After that, you can go to the [admin panel](http://localhost:8000/django/admin/)

2. **Adding a provider:** The superuser can add a new provider via the admin panel by specifying the API key. 
After saving the provider, the system automatically creates a background task 
that will fetch data from the provider every minute.

3. **Monitoring:** To get a list of saved blocks or search for blocks by UUID, currency, 
or block number, уou can use the API endpoints.
---

## API Endpoints
Once running, the API will be available at [localhost:8000](http://localhost:8000). \
Swagger UI documentation available [here](http://localhost:8000/docs/) and [here](http://localhost:8000/redoc/)

### Authentication
- **POST /auth/token/obtain/** - Obtain JWT token pair.
- **POST /auth/token/refresh/** - Refresh JWT access token.
- **POST /auth/register/** - Register a new user.
- **POST /auth/login/** - Login with user credentials.

### Blocks
- **GET /blocks/** - Retrieve all stored blocks (supports filtering by currency and provider).
- **GET /blocks/{block_uuid}/** - Retrieve block by ID (UUID).
- **GET /blocks/currency/{currency_name}/number/{block_number}/** - Retrieve block by currency and number.

### Providers
- **GET /providers/** - List available providers.
---

## License
This project is licensed under the MIT License.
