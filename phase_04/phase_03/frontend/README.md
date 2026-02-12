# VibeCode - Premium Task Management

This is the platform-agnostic version of the VibeCode task management application, optimized for deployment on Vercel and cross-platform compatibility.

## Changes Made for Platform Compatibility

1. **Next.js Version**: Downgraded from Next.js 16.1.4 to 14.2.22 to avoid Turbopack-related platform-specific dependencies
2. **SWC Bindings**: Removed Windows-specific SWC bindings that caused deployment issues
3. **Tailwind CSS**: Updated configuration to use standard plugins instead of platform-specific binaries
4. **CSS Imports**: Changed from Tailwind v4 syntax to v3 syntax for broader compatibility
5. **Dependencies**: Resolved various platform-specific dependency issues

## Getting Started

First, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Building for Production

To build the application for production:

```bash
npm run build
```

## Deploy on Vercel

The project is configured for easy deployment on Vercel:

1. Push the code to a Git repository
2. Connect your repository to Vercel
3. The build settings will be automatically detected

Or use the Vercel CLI:

```bash
npm i -g vercel
vercel
```

## Environment Variables

Make sure to set the following environment variables in your deployment environment:
- DATABASE_URL
- JWT_SECRET
- NEXTAUTH_URL
- NEXTAUTH_SECRET

## Notes

- This version removes platform-specific dependencies that were causing issues on Linux deployments
- The application maintains all original functionality while improving cross-platform compatibility
- All static pages are properly pre-rendered for optimal performance