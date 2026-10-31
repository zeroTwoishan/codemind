# CodeMind Vault - Learning Path

This document outlines the specific "bridge technologies" you need to learn to successfully complete Phase 1 through Phase 18 of the CodeMind Vault project. Since you already know React, Python, and Django Models, these tools will simply help you connect your frontend to your backend.

---

## 1. Django REST Framework (DRF)

### What it is
A toolkit that sits on top of standard Django. It automatically converts your Python database models (like a `Snippet`) into JSON data that your React frontend can read.

### Why we need it
Without DRF, you would have to manually write Python code to loop through database rows and format them as dictionaries before sending them to React.

### Mental Model
Think of DRF as a translator. 
*   **Serializer:** Translates a database row into JSON.
*   **ViewSet:** A pre-built controller that automatically handles `GET`, `POST`, `PUT`, and `DELETE` requests for that JSON.

---

## 2. SimpleJWT (JSON Web Tokens)

### What it is
A library for Django REST Framework that handles user logins without using traditional cookies/sessions.

### Why we need it
Because React and Django run on different ports (e.g., localhost:5173 vs localhost:8000), standard Django login sessions don't work well. JWT fixes this.

### Mental Model
When a user logs in, Django hands React a "VIP Pass" (a long string of text called an Access Token). React holds onto this pass in memory. Every time React wants to fetch private snippets, it flashes this VIP pass to Django in the request headers (`Authorization: Bearer <token>`).

---

## 3. TanStack Query (React Query)

### What it is
A data-fetching library for React. It completely replaces the standard `useEffect` + `fetch` + `useState` pattern.

### Why we need it
Managing loading states, error states, and caching data from a backend is tedious. TanStack Query does it all automatically in one hook.

### Mental Model
Instead of writing this:
```javascript
const [data, setData] = useState(null);
const [loading, setLoading] = useState(true);
useEffect(() => { fetch('/api/snippets').then(...) }, []);
```
You just write this:
```javascript
const { data, isLoading } = useQuery({ queryKey: ['snippets'], queryFn: fetchSnippets });
```

---

## 4. Monaco Editor (`@monaco-editor/react`)

### What it is
A React component that embeds the exact same code editor engine that powers VS Code directly into your web page.

### Why we need it
A standard `<textarea>` doesn't have syntax highlighting, line numbers, or auto-complete. We need a real code editor for a premium developer tool.

### Mental Model
It functions just like a massive, highly-customizable `<input>` field. You pass it a `value` (the code) and an `onChange` handler, and it handles all the beautiful syntax highlighting for you.

---

## 5. Google GenAI SDK (Python)

### What it is
A Python library provided by Google that lets your backend talk to Gemini (their AI model).

### Why we need it
To power the "AI Auto-Documenter" feature. 

### Mental Model
It's just a standard API request happening on the backend. 
1. React sends raw code to Django.
2. Django uses the GenAI SDK to send a prompt to Google: *"Format this code and add comments: [RAW CODE]"*.
3. Google sends back the formatted string.
4. Django sends that formatted string back to React.

---

### The Plan
Don't worry about memorizing these. The agent will write the implementation logic for these libraries, providing heavily commented code so you can learn their syntax by reading them in action within your own project.
