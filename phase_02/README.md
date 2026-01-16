# Todo Application

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 18+

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd F:\hackthone_todo_vibecode\phase_02\backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the backend directory with your database configuration:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
   BETTER_AUTH_SECRET=your-secret-key-here
   ```

4. Start the backend server:
   ```bash
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   Or run the batch file:
   ```bash
   start_backend.bat
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd F:\hackthone_todo_vibecode\phase_02\frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file in the frontend directory:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. Start the frontend development server:
   ```bash
   npm run dev
   ```

### Creating a Demo User
If you need to create a demo user for testing, run the following script in the backend directory:
```bash
python create_demo_user_fixed.py
```

This will create a user with:
- Email: `demo@example.com`
- Password: `demo123`

### Features
- Beautiful UI with gradient backgrounds and modern design
- Authentication with login/logout functionality
- Task management (create, read, update, delete tasks)
- Responsive design for all screen sizes
- Real-time task management

### Troubleshooting
- Make sure both backend and frontend servers are running
- Check that the ports are correct (backend: 8000, frontend: 3000)
- Verify that your database connection is working
- Ensure environment variables are properly set