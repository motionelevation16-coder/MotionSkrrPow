-- Subscribers table for human newsletter signups
-- Run this in Supabase SQL Editor

CREATE TABLE subscribers (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(100),
  categories TEXT[] DEFAULT '{}',  -- Array of category slugs they're interested in
  verified BOOLEAN DEFAULT false,
  unsubscribe_token VARCHAR(100) UNIQUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_subscribers_email ON subscribers(email);
CREATE INDEX idx_subscribers_verified ON subscribers(verified);

-- Enable RLS
ALTER TABLE subscribers ENABLE ROW LEVEL SECURITY;

-- Allow inserts (registration)
CREATE POLICY "Allow subscriber registration" ON subscribers
  FOR INSERT WITH CHECK (true);

-- Allow reading own subscription (via unsubscribe token)
CREATE POLICY "Allow reading subscribers" ON subscribers
  FOR SELECT USING (true);

-- Allow updates (for unsubscribe, verify, update preferences)
CREATE POLICY "Allow updating subscribers" ON subscribers
  FOR UPDATE USING (true);

-- Also allow creating new categories
CREATE POLICY "Allow creating categories" ON categories
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow updating categories" ON categories
  FOR UPDATE USING (true);
