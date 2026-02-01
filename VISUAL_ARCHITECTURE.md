# 🎨 CrawlX Frontend - Visual Architecture

## 📊 Component Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                      app/layout.tsx                         │
│  ┌───────────────────────────────────────────────────────┐ │
│  │              ThemeProvider                            │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │         ParticleBackground (3D)               │ │ │
│  │  │         (Three.js Animated Particles)          │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │              Navbar                             │ │ │
│  │  │  [Logo] [Dashboard] [Scraper] [Data] [Theme]   │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │              {children}                         │ │ │
│  │  │         (Page Content Below)                    │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 📄 Page Layouts

### Dashboard (app/page.tsx)
```
┌────────────────────────────────────────────────────┐
│                  Dashboard                         │
│  Your web scraping command center                 │
├────────────────────────────────────────────────────┤
│                                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────┐│
│  │ ⚡ Total │ │ 📊 Today │ │ 📰 News  │ │ 💼 Jobs││
│  │   Items  │ │  Scrapes │ │  Items   │ │ Listings││
│  │   1,234  │ │    45    │ │   856    │ │   378  ││
│  └──────────┘ └──────────┘ └──────────┘ └──────┘│
│                                                    │
│  ┌──────────────────────────────────────────────┐│
│  │          🚀 Run Scrapers Now                 ││
│  │  Fetch latest content from configured sources││
│  │             [Run Scrapers]                    ││
│  └──────────────────────────────────────────────┘│
│                                                    │
│  Quick Actions                                     │
│  ┌────────────────────┐ ┌────────────────────┐  │
│  │   🎯 Custom        │ │   📁 Data          │  │
│  │    Scraper         │ │   Explorer         │  │
│  │                    │ │                    │  │
│  │ Scrape any URL     │ │ Browse & export    │  │
│  │ with smart         │ │ your scraped data  │  │
│  │ extraction         │ │                    │  │
│  │                    │ │                    │  │
│  │  [Go to Scraper] → │ │  [Go to Explorer]→ │  │
│  └────────────────────┘ └────────────────────┘  │
│                                                    │
└────────────────────────────────────────────────────┘
```

### Custom Scraper (app/scraper/page.tsx)
```
┌────────────────────────────────────────────────────┐
│              Custom URL Scraper                    │
│  Scrape any website with AI-powered extraction    │
├────────────────────────────────────────────────────┤
│                                                    │
│  Enter Website URL                                 │
│  ┌──────────────────────────────────────────────┐│
│  │ https://example.com                          ││
│  └──────────────────────────────────────────────┘│
│                                                    │
│  Extraction Mode                                   │
│  ┌─────────────┐ ┌─────────┐ ┌──────┐ ┌────────┐│
│  │ ● Auto      │ │ Article │ │ Text │ │Structured││
│  └─────────────┘ └─────────┘ └──────┘ └────────┘│
│                                                    │
│  Wait Time (seconds)                               │
│  1 ●══════════════════════════════════════○ 10    │
│                        2s                          │
│                                                    │
│  ┌──────────────────────────────────────────────┐│
│  │            🚀 Scrape URL                     ││
│  └──────────────────────────────────────────────┘│
│                                                    │
│  ┌──────────────────────────────────────────────┐│
│  │ ✓ Scraped successfully!                      ││
│  │                                              ││
│  │ 📄 Metadata                                  ││
│  │ Title: Example Page                          ││
│  │ Author: John Doe                             ││
│  │ Published: 2024-01-01                        ││
│  │                                              ││
│  │ 📝 Content                                   ││
│  │ Lorem ipsum dolor sit amet, consectetur      ││
│  │ adipiscing elit. Sed do eiusmod tempor...    ││
│  │                                              ││
│  │ 📊 Tables Extracted: 3                       ││
│  │ 📋 Lists Extracted: 5                        ││
│  │                                              ││
│  │ [📋 Copy Content] [💾 Download]             ││
│  └──────────────────────────────────────────────┘│
│                                                    │
└────────────────────────────────────────────────────┘
```

### Data Explorer (app/data/page.tsx)
```
┌────────────────────────────────────────────────────┐
│              Data Explorer                         │
│  Browse, search, and export your scraped content  │
├────────────────────────────────────────────────────┤
│                                                    │
│  ┌──────────────────────────┐ ┌────────┐ ┌─────┐│
│  │ 🔍 Search titles...      │ │Tags ▼  │ │ ☰  ││
│  └──────────────────────────┘ └────────┘ └─────┘│
│  ☑ Fuzzy search                                   │
│                                                    │
│  [Search] [Reset] [Export CSV ▼] [Export PDF ▼]  │
│                                                    │
│  1,234 items found                                │
│                                                    │
│  ┌────────────────────────────────────────────────┐│
│  │Title         │Source│Tags    │Time   │Link   ││
│  ├────────────────────────────────────────────────┤│
│  │Intro to AI   │News  │tech,ai │2h ago │🔗     ││
│  │Python Tips   │News  │dev     │5h ago │🔗     ││
│  │Remote Senior │Jobs  │dev,rem │1d ago │🔗     ││
│  │Data Science  │News  │ai,data │2d ago │🔗     ││
│  │UI/UX Design  │Jobs  │design  │3d ago │🔗     ││
│  └────────────────────────────────────────────────┘│
│                                                    │
│  [← Previous]              [1] [2] [3]  [Next →]  │
│                                                    │
└────────────────────────────────────────────────────┘
```

## 🎨 Design System

### Color Palette
```
Primary Colors:
┌─────┬─────┬─────┬─────┬─────┐
│ 50  │ 100 │ 500 │ 600 │ 900 │
│#EEF2│#E0E7│#6366│#4F46│#312E│
│ FF  │ FE  │ F1  │ E5  │ 81  │
└─────┴─────┴─────┴─────┴─────┘
(Indigo shades)

Background:
Light:  #F9FAFB (gray-50)
Dark:   #0A0A0F (custom dark)

Text:
Light mode:  #111827 (gray-900)
Dark mode:   #F9FAFB (gray-50)
```

### Typography
```
Headings:
  h1: 2.25rem (36px) - font-bold
  h2: 1.875rem (30px) - font-bold
  h3: 1.5rem (24px) - font-semibold
  h4: 1.25rem (20px) - font-semibold

Body:
  Base: 1rem (16px) - font-normal
  Small: 0.875rem (14px)
  Tiny: 0.75rem (12px)

Font Family: Inter (Google Fonts)
```

### Spacing Scale
```
0.25rem (4px)   - xs
0.5rem (8px)    - sm
1rem (16px)     - base
1.5rem (24px)   - lg
2rem (32px)     - xl
3rem (48px)     - 2xl
4rem (64px)     - 3xl
```

### Border Radius
```
0.25rem (4px)   - rounded-sm
0.375rem (6px)  - rounded
0.5rem (8px)    - rounded-lg
0.75rem (12px)  - rounded-xl
1rem (16px)     - rounded-2xl
```

### Shadows
```
Card:
  box-shadow: 0 1px 3px rgba(0,0,0,0.1)

Card Hover:
  box-shadow: 0 10px 25px rgba(0,0,0,0.15)

Glow (Primary):
  box-shadow: 0 0 30px rgba(99,102,241,0.5)
```

## 🎭 Animations

### Float Animation
```css
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

Duration: 3s
Timing: ease-in-out
Iteration: infinite
```

### Glow Animation
```css
@keyframes glow {
  0%, 100% {
    box-shadow: 0 0 20px rgba(99,102,241,0.3);
  }
  50% {
    box-shadow: 0 0 30px rgba(99,102,241,0.6);
  }
}

Duration: 2s
Timing: ease-in-out
Iteration: infinite
```

### Fade In
```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

Duration: 0.5s
Timing: ease-out
```

## 🧩 Reusable CSS Classes

### Cards
```css
.card {
  background: white;
  dark:background: #1a1a24;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  transition: all 0.3s;
}

.card:hover {
  box-shadow: 0 10px 25px rgba(0,0,0,0.15);
  transform: translateY(-2px);
}
```

### Buttons
```css
.btn-primary {
  background: linear-gradient(to right, #6366f1, #a855f7);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-primary:hover {
  transform: scale(1.05);
  box-shadow: 0 10px 20px rgba(99,102,241,0.3);
}

.btn-secondary {
  background: transparent;
  color: #6366f1;
  border: 2px solid #6366f1;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
}
```

### Glass Effect
```css
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

Dark mode:
.glass {
  background: rgba(26, 26, 36, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
```

## 🌐 Responsive Breakpoints

```
Mobile:     320px - 639px   (default)
Tablet:     640px - 1023px  (sm:)
Desktop:    1024px - 1279px (lg:)
Large:      1280px+         (xl:)

Example:
<div className="
  grid 
  grid-cols-1      /* Mobile: 1 column */
  md:grid-cols-2   /* Tablet: 2 columns */
  lg:grid-cols-4   /* Desktop: 4 columns */
">
```

## 🎯 State Management

### Theme State (ThemeProvider)
```typescript
interface ThemeContext {
  theme: 'light' | 'dark' | 'system';
  setTheme: (theme: Theme) => void;
}

Storage: localStorage ('theme')
Default: 'system' (follows OS preference)
```

### Component State (useState)
```typescript
// Dashboard
const [stats, setStats] = useState({
  total: 0,
  today: 0,
  news: 0,
  jobs: 0
});

// Custom Scraper
const [url, setUrl] = useState('');
const [extractType, setExtractType] = useState('auto');
const [waitSeconds, setWaitSeconds] = useState(2);
const [result, setResult] = useState(null);
const [isLoading, setIsLoading] = useState(false);

// Data Explorer
const [items, setItems] = useState([]);
const [searchQuery, setSearchQuery] = useState('');
const [selectedTag, setSelectedTag] = useState('');
const [fuzzy, setFuzzy] = useState(false);
```

## 🔌 API Integration Flow

```
Frontend Component
      ↓
   apiClient (lib/api.ts)
      ↓
   Axios Request
      ↓
Backend API (http://localhost:8000)
      ↓
   FastAPI Route
      ↓
   CRUD Operation
      ↓
   PostgreSQL Database
      ↓
   Response
      ↓
   Frontend Update State
      ↓
   Re-render UI
```

## 📦 Build Output

### Development Build
```
npm run dev

Output:
- Hot reload enabled
- Source maps included
- Unoptimized bundles
- Fast refresh
- Port: 3000
```

### Production Build
```
npm run build

Output:
.next/
├── static/
│   ├── chunks/           # Code-split bundles
│   ├── css/             # Extracted CSS
│   └── media/           # Optimized images
├── server/
│   ├── app/             # Server components
│   └── pages/           # API routes
└── cache/              # Build cache

Size: ~2-3 MB (gzipped)
```

## 🚀 Performance Metrics

### Lighthouse Scores (Target)
```
Performance:  90+
Accessibility: 95+
Best Practices: 95+
SEO: 90+
```

### Core Web Vitals (Target)
```
LCP (Largest Contentful Paint):  < 2.5s
FID (First Input Delay):         < 100ms
CLS (Cumulative Layout Shift):   < 0.1
```

### Bundle Sizes
```
Main bundle:       ~150 KB (gzipped)
Three.js bundle:   ~120 KB (gzipped)
Total First Load:  ~300 KB (gzipped)
```

## 🎨 3D Particle System

### Configuration
```typescript
Particle Count: 5000
Radius: 1.5 (world units)
Size: 0.002 (point size)
Color: #6366f1 (primary indigo)
Rotation Speed:
  - X axis: delta / 10
  - Y axis: delta / 15
```

### Performance
```
FPS Target: 60 fps
WebGL Required: Yes
Fallback: None (graceful degradation)
CPU Usage: ~5-10% (idle)
```

This visual architecture shows exactly how CrawlX frontend is structured! 🎨✨
