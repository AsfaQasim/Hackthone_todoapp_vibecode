/**
 * Script to clear all authentication tokens and reset the application state
 */

console.log("Clearing all authentication tokens...");
console.log("Please close your browser windows to ensure all sessions are cleared.");

// Clear localStorage
if (typeof window !== 'undefined') {
    // Clear all auth-related items from localStorage
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_info');
    localStorage.removeItem('conversation_id');
    
    console.log("Cleared localStorage items:");
    console.log("- auth_token");
    console.log("- user_info"); 
    console.log("- conversation_id");
    
    // Clear cookies
    document.cookie.split(";").forEach(function(c) { 
        document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
    });
    
    console.log("Cleared all cookies");
} else {
    console.log("This script should be run in a browser environment");
}

console.log(" ");
console.log("IMPORTANT: Please restart both frontend and backend servers now.");
console.log("Then clear your browser cache and restart your browser completely.");
console.log("Finally, log in again with your credentials.");