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

### Authentication & User Isolation
The application implements a secure, stateless authentication system:

- JWT-based authentication using Better Auth on the frontend
- Cryptographic verification of JWT tokens on the backend
- User isolation at the API level - users can only access their own data
- All protected endpoints require a valid JWT token
- Requests without valid tokens return HTTP 401
- Requests with mismatched user IDs return HTTP 403

### API Endpoints

The application provides the following API endpoints:

- `GET /health` - Health check
- `GET /profile` - Get authenticated user profile (requires JWT)
- `GET /todos/` - Get all todos for the authenticated user (requires JWT)
- `POST /todos/` - Create a new todo (requires JWT)
- `GET /todos/{id}` - Get a specific todo (requires JWT)
- `PUT /todos/{id}` - Update a specific todo (requires JWT)
- `DELETE /todos/{id}` - Delete a specific todo (requires JWT)
- `DELETE /todos/` - Delete all todos for the authenticated user (requires JWT)

### Features
- Beautiful UI with gradient backgrounds and modern design
- Authentication with login/logout functionality
- Task management (create, read, update, delete tasks)
- Secure user isolation - users can only access their own data
- Responsive design for all screen sizes
- Real-time task management

### Troubleshooting
- Make sure both backend and frontend servers are running
- Check that the ports are correct (backend: 8000, frontend: 3000)
- Verify that your database connection is working
- Ensure environment variables are properly set, especially `BETTER_AUTH_SECRET`