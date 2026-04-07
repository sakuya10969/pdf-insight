# UI Design — PDF Ingest & Search System

## Overview

White-based, clean interface using Mantine UI v9. Minimal custom styling — lean on Mantine defaults and components. Root layout handles global structure so individual pages only worry about their own content.

## Root Layout Structure

```
┌─────────────────────────────────────────────┐
│  AppShell.Header                            │
│  [Logo/Title]                    [Nav links]│
├────────────────┬────────────────────────────┤
│  AppShell      │  AppShell.Main             │
│  .Navbar       │                            │
│  (optional)    │  <Outlet />                │
│                │  (page content here)       │
│                │                            │
├────────────────┴────────────────────────────┤
│  AppShell.Footer (optional)                 │
└─────────────────────────────────────────────┘
```

Use `AppShell` in `root.tsx` so every route inherits the layout automatically. No per-page layout wrappers needed.

### AppShell Config

- `header.height`: 60
- `navbar.width`: 250 (collapsible, hidden on mobile)
- `padding`: "md"
- Background: white (`#ffffff`)

## Color & Theme

- Base background: white
- Primary color: Mantine default blue (`blue.6`)
- Text: Mantine default dark
- No dark mode for now
- Use `MantineProvider` with `defaultColorScheme="light"`

## Key Mantine Components

These are the components expected to be used across the app:

| Component | Usage |
|-----------|-------|
| `AppShell` | Root layout (header, navbar, main) |
| `Button` | Primary actions (upload, search, send) |
| `TextInput` | Search query input |
| `FileInput` / Dropzone | PDF file upload |
| `Card` | Document list items, search result cards |
| `Text` / `Title` | Typography |
| `Stack` / `Group` / `Flex` | Layout utilities |
| `Loader` / `Skeleton` | Loading states |
| `Notification` | Upload success/error feedback |
| `ScrollArea` | Chat/results scrollable area |
| `Badge` | Document status, chunk count |
| `ActionIcon` | Icon buttons (delete, refresh) |
| `NavLink` | Sidebar navigation items |

## Pages

### PDF Upload Page
- Dropzone area (drag & drop or click)
- Upload progress indicator
- List of uploaded documents (Card with title, status Badge)

### Search / Chat Page
- TextInput + Button for query submission
- Results area: Stack of Cards showing matched chunks
- LLM answer section below results

### Document List (Navbar or dedicated page)
- NavLink items per document
- Badge showing processing status
- ActionIcon for delete

## Spacing & Layout Rules

- Use Mantine spacing scale: `xs`, `sm`, `md`, `lg`, `xl`
- Default page padding: `md`
- Card padding: `md`
- Stack spacing between sections: `lg`
- Keep max content width reasonable (~900px) using `Container` with `size="md"`

## Guidelines

- Don't override Mantine styles unless absolutely necessary
- Use `variant="light"` for secondary buttons
- Use `variant="filled"` for primary actions
- Keep the interface minimal — no decorative elements
- Loading states are required for all async operations
