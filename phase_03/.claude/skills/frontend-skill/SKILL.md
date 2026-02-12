---
name: frontend-skill
description: Build frontend pages, components, layouts, and styling for modern web applications.
---

# Frontend Skill – UI & Layout Development

## Instructions

1. **Page Structure**
   - Build pages using a clear and consistent structure
   - Use semantic HTML elements
   - Organize pages according to routing conventions

2. **Component Development**
   - Create reusable and composable UI components
   - Keep components small and focused
   - Pass props clearly and consistently

3. **Layout Design**
   - Implement responsive layouts
   - Use flexbox and grid appropriately
   - Handle spacing, alignment, and positioning carefully

4. **Styling**
   - Apply consistent styling across the application
   - Use modern CSS or utility-first frameworks
   - Ensure accessibility and contrast standards

## Best Practices
- Follow mobile-first design principles
- Keep components reusable and maintainable
- Avoid inline styles when possible
- Use consistent spacing and typography
- Ensure responsive behavior on all screen sizes
- Follow frontend and accessibility best practices

## Example Structure
```tsx
export default function Page() {
  return (
    <main className="container">
      <h1 className="title">Page Title</h1>
      <p className="description">Content goes here</p>
    </main>
  );
}
