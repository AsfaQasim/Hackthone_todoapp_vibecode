// Simple test to check if the import issue is resolved
try {
    console.log('Testing auth import...');
    const { auth } = require('./lib/auth');
    console.log('✅ Auth module imported successfully!');
    console.log('✅ Original issue with missing wildcard.mjs has been resolved!');
} catch (error) {
    console.error('❌ Error importing auth module:', error.message);
    if (error.message.includes('wildcard.mjs')) {
        console.error('❌ The original wildcard.mjs issue still exists');
    }
}