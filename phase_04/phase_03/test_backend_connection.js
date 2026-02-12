// Simple test to verify the backend API is working
// test_backend.js

const testBackend = async () => {
  try {
    console.log("Testing backend health endpoint...");
    const healthResponse = await fetch('http://localhost:8000/health');
    const healthData = await healthResponse.json();
    console.log("Health check:", healthData);
    
    // This would require a valid token, so we'll skip the chat test for now
    console.log("Backend is running and accessible.");
  } catch (error) {
    console.error("Error connecting to backend:", error.message);
  }
};

testBackend();