/**
 * Wildcard matching utility function
 * This is a temporary workaround for the missing wildcard.mjs file issue
 */
export function wildcardMatch(pattern, str) {
    if (pattern === '*') {
        return true;
    }

    // Handle multiple patterns separated by commas
    const patterns = pattern.split(',');
    
    for (let p of patterns) {
        p = p.trim();
        
        // Escape special regex characters except for * and ?
        const regexPattern = p.replace(/[.+^${}()|[\]\\]/g, '\\$&')
                              .replace(/\*/g, '.*')
                              .replace(/\?/g, '.');
        
        const regex = new RegExp(`^${regexPattern}$`);
        if (regex.test(str)) {
            return true;
        }
    }
    
    return false;
}