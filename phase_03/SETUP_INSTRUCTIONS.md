# VibeCode Task Manager - Setup Instructions

## Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- pip package manager

## Setup Instructions

### 1. Backend Setup

1. Navigate to the backend directory:
```bash
cd F:\hackthone_todo_vibecode\phase_03\backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
python main.py
```

The backend will start on `http://localhost:8000`

### 2. Frontend Setup

1. Navigate to the frontend directory:
```bash
cd F:\hackthone_todo_vibecode\phase_03\frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the frontend development server:
```bash
npm run dev
```

The frontend will start on `http://localhost:3000`

## Important Notes

- The backend must be running on port 8000 for the AI assistant features to work
- The frontend runs on port 3000 and proxies chat requests to the backend
- Make sure both servers are running simultaneously for full functionality
- The AI assistant requires a valid authentication token to function

## Troubleshooting

If the chat UI appears to be loading indefinitely:
1. Verify that the backend server is running on port 8000
2. Check that the frontend can connect to the backend
3. Ensure your authentication token is valid and properly formatted