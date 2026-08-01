# LeadRadar AI Design System

This document is the **Single Source of Truth** for all frontend styling. Do **NOT** invent new styles, colors, or animations outside of this system.

## 1. Aesthetic Identity
- **Vibe**: Modern B2B SaaS, Professional, High-Contrast, Data-Dense but Breathable.
- **Theme**: Light Mode default, with full Dark Mode support using `next-themes`.
- **Key Elements**: Glassmorphism (on sidebars/headers), soft shadows, rounded corners, crisp typography.

## 2. Typography
We use **Inter** (default sans) for UI elements and **Cal Sans** (or similar Display font) for prominent headers.

- `h1`: text-3xl font-bold tracking-tight
- `h2`: text-2xl font-semibold tracking-tight
- `h3`: text-xl font-semibold tracking-tight
- `body`: text-sm text-slate-700 dark:text-slate-300
- `muted`: text-sm text-slate-500 dark:text-slate-400

## 3. Color Palette (Tailwind)

**Primary (Brand)**:
- `primary`: Violet-600 (`#7c3aed`)
- `primary-foreground`: White (`#ffffff`)

**Background & Surface**:
- `background`: Slate-50 (Light) / Slate-950 (Dark)
- `card`: White (Light) / Slate-900 (Dark)
- `border`: Slate-200 (Light) / Slate-800 (Dark)

**Semantic Status Colors**:
- `success`: Emerald-500 (e.g., High Intent)
- `warning`: Amber-500 (e.g., Medium Intent)
- `destructive`: Rose-500 (e.g., Low Intent, Errors)
- `info`: Blue-500 (e.g., Crawler running)

## 4. UI Components (shadcn/ui)

### Cards
- **Style**: `rounded-xl border bg-card text-card-foreground shadow-sm`
- **Usage**: Used for statistics, charts, and wrapping tables.

### Buttons
- **Primary**: `bg-primary text-primary-foreground hover:bg-primary/90`
- **Secondary**: `bg-secondary text-secondary-foreground hover:bg-secondary/80`
- **Outline**: `border border-input bg-background hover:bg-accent hover:text-accent-foreground`
- **Ghost**: `hover:bg-accent hover:text-accent-foreground`

### Tables
- **Style**: Professional, full-width, clear borders on headers, hover effects on rows.
- **Row Hover**: `hover:bg-muted/50 transition-colors`
- **Pagination**: Standard numbered pagination with Next/Prev buttons.

## 5. Effects & Animations

### Glassmorphism
Used exclusively for sticky navbars or floating elements.
- `backdrop-blur-md bg-background/80`

### Micro-interactions
All interactive elements must have a transition.
- `transition-all duration-200 ease-in-out`

## 6. Layout & Spacing
- **Sidebar Width**: `w-64` (desktop)
- **Container Max-Width**: `max-w-7xl`
- **Page Padding**: `p-6` or `p-8`
- **Gap Standard**: `gap-4` for tight groups, `gap-6` for larger sections.

## Enforcement
When building new pages or components, ALWAYS refer to these Tailwind classes. If you need a new component, install it via `npx shadcn@latest add <component>`.
