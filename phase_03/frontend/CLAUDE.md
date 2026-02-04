# Frontend Guidelines

## Stack
- Next.js 16 (App Router)
- TypeScript
- Tailwind CSS
- Better Auth

## Patterns
- Use server components by default
- Client components only when needed (interactivity)
- API calls go through `/lib/api.ts`

## Component Structure
- `/components` - Reusable UI components
- `/app` - Pages and layouts

## API Client
All backend calls should use the api client:

```typescript
import { api } from '@/lib/api'
const tasks = await api.getTasks()
```

## Styling
- Use Tailwind CSS classes
- No inline styles
- Follow existing component patterns
