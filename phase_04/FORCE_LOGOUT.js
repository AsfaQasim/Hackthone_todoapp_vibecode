// Run this in browser console on http://localhost:3000
// This will clear all tokens and force logout

console.log('=== FORCE LOGOUT ===');

// Clear all cookies
document.cookie.split(";").forEach(function(c) { 
    document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
});

// Clear storage
localStorage.clear();
sessionStorage.clear();

console.log('✅ All tokens cleared!');
console.log('Now refresh the page and login again');

// Redirect to login
window.location.href = '/login';
