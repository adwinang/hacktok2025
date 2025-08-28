# Hacktok Backend

A simple Python backend running on FastAPI.

## Prerequisites

Ensure pip is using the latest version (should be 25.x):

```bash
python -m pip install --upgrade pip
```

## Local Development

### 1. Set up Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

```bash
cp .env.example .env
```

Edit the `.env` file and update:

- `MONGO_URI` with your MongoDB connection string

### 5. Run the Application

```bash
python main.py
```

## Docker Alternative

### Build and Run

```bash
docker build -t hacktok-backend .
docker run --env-file .env -p 8000:8000 hacktok-backend
```

**Note:** Ensure your `.env` file is properly configured before running the docker command.
