# CrawlX Frontend

Modern Next.js 14 frontend for the CrawlX data scraping platform with 3D effects and dark mode.

## ✨ Features

### 🎨 Modern UI
- **Dark/Light Mode** - Seamless theme switching with system preference detection
- **3D Particle Background** - Interactive Three.js particle field animation
- **Glassmorphism** - Beautiful glass-effect cards and panels
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile

### 📊 Dashboard
- Real-time statistics display
- Quick scraper controls
- Navigation to all features
- Animated stat cards with icons

### 🔍 Custom URL Scraper
- Scrape ANY website URL
- Smart content extraction modes:
  - **Auto** - Automatically detects best extraction method
  - **Article** - Optimized for news articles and blog posts
  - **Text** - Extracts all visible text content
  - **Structured** - Extracts tables, lists, and structured data
- Adjustable wait time (1-10 seconds)
- Real-time scraping status
- Copy or download results
- Displays metadata (title, author, published date)
- Shows extracted tables and lists

### 📁 Data Explorer
- Browse all scraped items
- **Fuzzy Search** - Find content even with typos
- Tag filtering (news, tech, jobs, remote)
- Export to CSV or PDF
- Sortable data table
- View full content details
- Direct links to source URLs

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm
- Backend API running on http://localhost:8000

### Installation

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run development server:
```bash
npm run dev
```

3. Open http://localhost:3000 in your browser

### Production Build

```bash
npm run build
npm start
```

## 📁 Project Structure

```
frontend/
├── app/                    # Next.js 14 App Router
│   ├── page.tsx           # Dashboard (/)
│   ├── scraper/           # Custom URL scraper (/scraper)
│   │   └── page.tsx
│   ├── data/              # Data explorer (/data)
│   │   └── page.tsx
│   ├── layout.tsx         # Root layout with 3D background
│   └── globals.css        # Global styles
├── components/
│   ├── 3d/                # Three.js components
│   │   └── ParticleBackground.tsx
│   ├── layout/            # Layout components
│   │   └── Navbar.tsx
│   └── providers/         # React providers
│       └── ThemeProvider.tsx
├── lib/
│   └── api.ts             # API client for backend
├── types/
│   └── index.ts           # TypeScript interfaces
└── public/                # Static assets
```

## 🎨 Technology Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **3D Graphics**: Three.js + @react-three/fiber + @react-three/drei
- **Animations**: Framer Motion
- **State**: Zustand
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Date Formatting**: date-fns

## 🔌 API Integration

The frontend connects to the backend API at `http://localhost:8000`:

```typescript
// lib/api.ts
const API_BASE = 'http://localhost:8000';

// Available methods:
apiClient.getItems(params)          // Get scraped items
apiClient.searchItems(params)       // Search with fuzzy matching
apiClient.runScrapers(spiders)      // Run news/jobs scrapers
apiClient.scrapeUrl(data)           // Custom URL scraper
apiClient.exportJSON()              // Export as JSON
apiClient.exportCSV()               // Export as CSV
apiClient.exportPDF(options)        // Export as PDF
```

## 🎯 Pages

### Dashboard (/)
- Total items count
- Today's scrapes count
- News and jobs counters
- Quick actions to run scrapers
- Navigation to features

### Custom Scraper (/scraper)
- URL input field
- Extraction mode selector
- Wait time slider
- Scrape button
- Results display with metadata
- Copy/download buttons
- Tables and lists extraction

### Data Explorer (/data)
- Search bar with fuzzy search
- Tag filter dropdown
- Export CSV/PDF buttons
- Data table with:
  - Title and summary
  - Source information
  - Tags display
  - Relative timestamps
  - External links

## 🎨 Styling Features

### Dark Mode
```tsx
// Automatic theme detection
const { theme, setTheme } = useTheme()
```

### Custom Animations
```css
.animate-float    /* Floating cards */
.animate-glow     /* Glowing effects */
.glass            /* Glassmorphism */
```

### Tailwind Extensions
```js
// Custom colors, animations, and utilities
primary-500, dark-bg, glass effect
```

## 🐛 Troubleshooting

### Backend Connection Issues
- Ensure backend is running on http://localhost:8000
- Check CORS settings in backend/main.py
- Verify API endpoints are accessible

### 3D Background Not Loading
- Three.js components use dynamic imports with `ssr: false`
- Check browser console for WebGL errors
- Ensure browser supports WebGL

### Build Errors
```bash
rm -rf .next node_modules
npm install
npm run build
```

## 📝 Development Tips

1. **Hot Reload**: Changes auto-reload during development
2. **TypeScript**: All components are fully typed
3. **ESLint**: Run `npm run lint` to check code quality
4. **API Mocking**: Update `lib/api.ts` to use mock data for testing

## 🚀 Performance

- **Static Generation**: Dashboard and static pages pre-rendered
- **Dynamic Imports**: 3D components loaded only when needed
- **Image Optimization**: Next.js automatic image optimization
- **Code Splitting**: Automatic route-based code splitting

## 📄 License

Part of the CrawlX Data Scraping Project

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request
