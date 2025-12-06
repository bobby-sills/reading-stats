# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A reading progress tracker that syncs with KOReader and displays book reading statistics via a Svelte-based web interface. The application combines Python scripts for data syncing with a Svelte 5 + TypeScript frontend.

## Development Commands

### Frontend Development
- `npm run dev` - Start Vite development server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run check` - Run type checking with svelte-check and TypeScript

### Data Syncing
- `python scripts/sync_koreader.py` - Sync reading progress from KOReader database via Google Drive
  - Requires `GOOGLE_CREDENTIALS` and `FILE_ID` environment variables
  - Downloads KOReader SQLite database, extracts reading progress, writes to `data/koreader-data.json`
  - Currently filters for specific books defined in `books_to_track` list

## Architecture

### Data Flow
1. KOReader stores reading progress in SQLite database (`page_stat_data`, `book` tables)
2. `scripts/sync_koreader.py` downloads database from Google Drive, queries latest reading session per book, outputs filtered JSON
3. Svelte app imports JSON data files directly (`koreader-data.json`, `manual-data.json`)
4. `App.svelte` renders progress bars for each book using `ProgressBar.svelte` component

### Data Structure
Books are stored as JSON with this schema:
```json
{
  "updated_at": "ISO 8601 timestamp",
  "books": [
    {
      "title": "Book Title",
      "authors": "Author Name",
      "percentage_completed": 45.67
    }
  ]
}
```

### Frontend Structure
- **Svelte 5** with runes API (`$props()` syntax)
- Components in `src/lib/`
- Gruvbox Dark color scheme via CSS variables (`--fg`, `--bg3`, `--green`, etc.) defined in `src/styles/gruvbox-dark.css`
- Vite for bundling, TypeScript for type safety

## Key Implementation Notes

### Python Sync Script
- Queries for latest reading session per book using subquery on `MAX(start_time)`
- Column mapping quirk: query result `row[1]` is title, `row[2]` is authors (due to SELECT column order)
- Currently hardcoded to filter for specific books in `books_to_track` list
- Creates `data/` directory if missing before writing JSON

### Svelte Components
- `ProgressBar.svelte` uses Svelte 5 runes (`$props()`) not Svelte 4 export syntax
- Progress calculation: `Math.ceil((percent / 100) * totalPages)` to show page count
- CSS custom properties for theming instead of hardcoded colors
- Note: `totalPages` is currently hardcoded to "1000" in App.svelte, not pulled from data

### Type Definitions
- Book interface defined in `App.svelte` (not shared type file)
- Properties: `title: string`, `authors: string`, `percentage_completed: number`
