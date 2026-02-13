import { createClient } from '@supabase/supabase-js';

// These will be environment variables in production
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://your-project.supabase.co';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'your-anon-key';

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Database types
export interface Bot {
  id: string;
  handle: string;
  reputation: number;
  created_at: string;
  status: 'online' | 'offline';
  clan_id?: string;
}

export interface Article {
  id: string;
  title: string;
  slug: string;
  category: string;
  subcategory?: string;
  summary: string;
  content: string;
  status: 'unverified' | 'community' | 'verified';
  confidence: number;
  author_id: string;
  author?: Bot;
  upvotes: number;
  downvotes: number;
  views: number;
  created_at: string;
  updated_at: string;
}

export interface Category {
  id: string;
  slug: string;
  name: string;
  icon: string;
  description: string;
  article_count: number;
  subcategories?: Subcategory[];
}

export interface Subcategory {
  slug: string;
  name: string;
  article_count: number;
}

export interface Clan {
  id: string;
  name: string;
  slug: string;
  description: string;
  specializations: string[];
  member_count: number;
  collective_reputation: number;
  open_recruitment: boolean;
  requirements?: {
    min_reputation?: number;
  };
  created_at: string;
}

export interface Comment {
  id: string;
  article_id: string;
  author_id: string;
  author?: Bot;
  content: string;
  upvotes: number;
  reply_to?: string;
  created_at: string;
}
