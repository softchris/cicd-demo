---
name: frontend
description: Builds and maintains React TypeScript frontend applications following modern best practices
argument-hint: Feature requests, bug fixes, component creation, styling tasks, or frontend architecture questions
tools: ['vscode', 'execute', 'read', 'agent', 'edit', 'search', 'web', 'todo']
---

# Frontend Agent Guidelines

## Framework & Dependencies

- **UI Framework**: React 18+ with TypeScript
- **Build Tool**: Vite (preferred) or Create React App
- **Package Manager**: npm or yarn (be consistent within project)
- **TypeScript Version**: 5.0+
- **Testing Framework**: Jest + React Testing Library
- **Linting**: ESLint with TypeScript support
- **Formatting**: Prettier
- **CSS Solution**: CSS Modules, Tailwind CSS, or styled-components (follow project convention)

## Code Style & Conventions

### Naming Conventions
- **Components**: PascalCase (e.g., `UserProfile.tsx`, `NavigationBar.tsx`)
- **Files**: Match component name: `UserProfile.tsx` for the `UserProfile` component
- **Hooks**: camelCase starting with "use" (e.g., `useAuth`, `useFetchData`)
- **Utilities**: camelCase (e.g., `formatDate`, `validateEmail`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `API_BASE_URL`, `MAX_RETRY_ATTEMPTS`)
- **Types/Interfaces**: PascalCase (e.g., `User`, `ApiResponse`, `ButtonProps`)

### TypeScript Usage
- **Strict Mode**: Enable `strict: true` in `tsconfig.json`
- **Type Everything**: Avoid `any` - use `unknown` if type is truly unknown
- **Props Typing**: Define interfaces for component props
  ```typescript
  interface ButtonProps {
    label: string;
    onClick: () => void;
    variant?: 'primary' | 'secondary';
    disabled?: boolean;
  }
  ```
- **Event Handlers**: Use React's built-in types
  ```typescript
  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => { }
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => { }
  ```
- **Generics**: Use for reusable components and hooks
- **Type vs Interface**: Prefer `interface` for component props and public APIs, `type` for unions and complex types

### Component Structure

#### Functional Components
- Use functional components with hooks (no class components)
- Export component as default or named export (be consistent)
- Structure order:
  1. Imports
  2. Type definitions
  3. Component function
  4. Styled components / CSS (if applicable)
  5. Export statement

Example:
```typescript
import React, { useState, useEffect } from 'react';
import styles from './UserProfile.module.css';

interface UserProfileProps {
  userId: string;
  onUpdate?: (user: User) => void;
}

export const UserProfile: React.FC<UserProfileProps> = ({ userId, onUpdate }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch user data
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  if (!user) return <div>User not found</div>;

  return (
    <div className={styles.container}>
      {/* Component JSX */}
    </div>
  );
};
```

### Custom Hooks
- Extract reusable logic into custom hooks
- Prefix with "use"
- Return arrays for simple state or objects for complex state
- Include TypeScript generics where appropriate
  ```typescript
  function useFetch<T>(url: string): { data: T | null; loading: boolean; error: Error | null } {
    // Implementation
  }
  ```

## State Management

- **Local State**: `useState` for component-level state
- **Side Effects**: `useEffect` for data fetching, subscriptions
- **Context API**: For shared state across multiple components
- **State Libraries**: Use Redux Toolkit, Zustand, or Jotai if needed (check project)
- **Form State**: Consider React Hook Form or Formik for complex forms

### State Best Practices
- Keep state as local as possible
- Lift state up only when necessary
- Use `useReducer` for complex state logic
- Memoize expensive computations with `useMemo`
- Memoize callbacks with `useCallback` when passing to child components

## Styling

### CSS Organization
- **CSS Modules**: Scope styles to components (`ComponentName.module.css`)
- **Tailwind CSS**: Use utility classes, create custom components for repeated patterns
- **Styled Components**: Co-locate styles with components
- **Global Styles**: Minimal; use for resets and theme variables

### Styling Best Practices
- Follow mobile-first responsive design
- Use CSS variables for theming
- Maintain consistent spacing scale (e.g., 4px, 8px, 16px, 24px, 32px)
- Use semantic color names (e.g., `primary`, `danger`, not `blue`, `red`)
- Ensure accessibility (contrast ratios, focus states)

## Testing

### Test File Organization
- Place tests next to components: `Button.test.tsx` alongside `Button.tsx`
- Or use `__tests__` directory: `__tests__/Button.test.tsx`

### Testing Patterns
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders with correct label', () => {
    render(<Button label="Click me" onClick={() => {}} />);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick handler when clicked', () => {
    const handleClick = jest.fn();
    render(<Button label="Click" onClick={handleClick} />);
    fireEvent.click(screen.getByText('Click'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button label="Click" onClick={() => {}} disabled />);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

### Testing Best Practices
- Test user behavior, not implementation details
- Use `screen.getByRole` for better accessibility
- Test error states and edge cases
- Mock API calls and external dependencies
- Aim for meaningful tests, not 100% coverage

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.module.css
│   │   └── Button.test.tsx
│   └── Input/
├── pages/              # Page-level components (if using routing)
│   ├── Home.tsx
│   └── UserProfile.tsx
├── hooks/              # Custom hooks
│   ├── useAuth.ts
│   └── useFetch.ts
├── utils/              # Utility functions
│   ├── formatters.ts
│   └── validators.ts
├── services/           # API calls and external services
│   └── api.ts
├── types/              # Shared TypeScript types
│   └── index.ts
├── contexts/           # React contexts
│   └── AuthContext.tsx
├── constants/          # Constants and configuration
│   └── config.ts
├── assets/             # Images, fonts, static files
└── App.tsx            # Root component
```

## API Integration

- Centralize API calls in a `services` directory
- Use `fetch` or axios for HTTP requests
- Handle loading, error, and success states
- Use environment variables for API URLs (e.g., `VITE_API_URL`)
- Implement proper error handling with try-catch
- Consider using React Query or SWR for data fetching

Example:
```typescript
// services/api.ts
const API_BASE_URL = import.meta.env.VITE_API_URL;

export async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`${API_BASE_URL}/users/${id}`);
  if (!response.ok) {
    throw new Error('Failed to fetch user');
  }
  return response.json();
}
```

## Accessibility (a11y)

- Use semantic HTML elements
- Provide `alt` text for images
- Ensure keyboard navigation works
- Use ARIA attributes when necessary
- Test with screen readers
- Maintain proper heading hierarchy
- Ensure sufficient color contrast

## Performance Optimization

- Code splitting with `React.lazy` and `Suspense`
- Lazy load images and heavy components
- Memoize expensive operations with `useMemo`
- Prevent unnecessary re-renders with `React.memo`
- Use proper key props in lists
- Optimize bundle size (analyze with tools like Vite Bundle Analyzer)

## Environment & Configuration

- Use `.env` files for environment variables
- Prefix variables: `VITE_*` for Vite, `REACT_APP_*` for CRA
- Never commit `.env` files with secrets
- Document required environment variables in README

## Build & Development

### Scripts (package.json)
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "test": "jest",
    "test:watch": "jest --watch",
    "lint": "eslint . --ext ts,tsx",
    "format": "prettier --write \"src/**/*.{ts,tsx,css}\""
  }
}
```

### Development Workflow
1. Run `npm install` to install dependencies
2. Run `npm run dev` to start development server
3. Run `npm run lint` before committing
4. Run `npm test` to ensure tests pass
5. Run `npm run build` to verify production build

## Error Handling

- Use Error Boundaries for component-level errors
- Display user-friendly error messages
- Log errors to console in development
- Integrate error tracking (e.g., Sentry) in production
- Handle async errors with try-catch
- Provide fallback UI for error states

## Best Practices

- **Keep components small**: Single responsibility principle
- **Props drilling**: Avoid deep prop passing; use Context or state management
- **Dependencies**: Keep `useEffect` dependencies accurate
- **Keys in lists**: Use stable, unique keys (avoid array indices)
- **Immutability**: Never mutate state directly
- **TypeScript**: Leverage the type system; avoid disabling checks
- **Comments**: Write self-documenting code; comment only complex logic
- **Code reviews**: Follow the project's review process
- **Security**: Sanitize user input, avoid XSS vulnerabilities
- **Performance**: Profile before optimizing; avoid premature optimization