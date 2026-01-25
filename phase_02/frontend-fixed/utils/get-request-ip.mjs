/**
 * Utility to get IP address from request
 * This is a temporary workaround for the missing get-request-ip.mjs file issue
 */
export function getIp(request) {
    // Try different headers that might contain the client IP
    const forwarded = request.headers.get('x-forwarded-for');
    const realIp = request.headers.get('x-real-ip');
    const cfConnectingIp = request.headers.get('cf-connecting-ip');
    
    // Parse the first IP from x-forwarded-for if it exists
    if (forwarded) {
        const ips = forwarded.split(',').map(ip => ip.trim());
        return ips[0] || null;
    }
    
    // Return other possible IP headers
    if (realIp) return realIp;
    if (cfConnectingIp) return cfConnectingIp;
    
    // For development purposes, return localhost if no header is found
    // In a real environment, you might want to handle this differently
    return '127.0.0.1';
}