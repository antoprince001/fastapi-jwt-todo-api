# Todo API - FastAPI + JWT Auth

## Steps to run locally

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Run the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
```

## Steps to run via Docker

1. Build the Docker image:

```bash
docker build -t fastapi_todo .
```

2. Run the Docker container:

```bash
docker run -d --name fast_api_container -p 8080:8080 \
-e secret_key=<test_key> \
-e test_hashed_password='<demo_user_hashed_pwd>' \
fastapi_todo
```

Replace `<test_key>` with your secret key and `<demo_user_hashed_pwd>` with the hashed password for the demo user.

```plaintext
Note: Ensure Docker is installed on your system before running the Docker commands.
```

