-- Enable PostgreSQL pg_trgm extension for fuzzy text search
-- This extension provides functions and operators for determining the similarity of text based on trigram matching

-- Create the extension if it doesn't exist
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Create GIN index on title for faster fuzzy search
CREATE INDEX IF NOT EXISTS idx_scraped_items_title_trgm ON scraped_items USING gin (title gin_trgm_ops);

-- Create GIN index on summary for faster fuzzy search
CREATE INDEX IF NOT EXISTS idx_scraped_items_summary_trgm ON scraped_items USING gin (summary gin_trgm_ops);

-- Create GIN index on tags for faster tag filtering
CREATE INDEX IF NOT EXISTS idx_scraped_items_tags ON scraped_items USING gin (tags);
