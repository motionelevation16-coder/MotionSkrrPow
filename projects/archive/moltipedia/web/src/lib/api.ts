import { supabase } from './supabase';
import type { Article, Category, Bot } from './supabase';

// Fetch all categories with article counts
export async function getCategories(): Promise<Category[]> {
  const { data, error } = await supabase
    .from('categories')
    .select('*, parent_id')
    .order('name', { ascending: true });
  
  if (error) {
    console.error('Error fetching categories:', error);
    return [];
  }
  
  return data || [];
}

// Fetch a single category by slug
export async function getCategoryBySlug(slug: string): Promise<Category | null> {
  const { data, error } = await supabase
    .from('categories')
    .select('*')
    .eq('slug', slug)
    .single();
  
  if (error) {
    console.error('Error fetching category:', error);
    return null;
  }
  
  return data;
}

// Fetch articles for a category
export async function getArticlesByCategory(categorySlug: string): Promise<Article[]> {
  // First get the category ID
  const category = await getCategoryBySlug(categorySlug);
  if (!category) return [];
  
  const { data, error } = await supabase
    .from('articles')
    .select(`
      *,
      author:bots(id, handle, reputation)
    `)
    .eq('category_id', category.id)
    .order('upvotes', { ascending: false });
  
  if (error) {
    console.error('Error fetching articles:', error);
    return [];
  }
  
  return data || [];
}

// Fetch trending articles (most upvoted recent articles)
export async function getTrendingArticles(limit: number = 5): Promise<Article[]> {
  const { data, error } = await supabase
    .from('articles')
    .select(`
      *,
      author:bots(id, handle, reputation)
    `)
    .order('upvotes', { ascending: false })
    .limit(limit);
  
  if (error) {
    console.error('Error fetching trending articles:', error);
    return [];
  }
  
  return data || [];
}

// Fetch a single article by slug
export async function getArticleBySlug(slug: string): Promise<Article | null> {
  const { data, error } = await supabase
    .from('articles')
    .select(`
      *,
      author:bots(id, handle, reputation),
      category:categories(id, slug, name, icon)
    `)
    .eq('slug', slug)
    .single();
  
  if (error) {
    console.error('Error fetching article:', error);
    return null;
  }
  
  return data;
}

// Fetch site stats
export async function getSiteStats() {
  // Get article count
  const { count: articleCount } = await supabase
    .from('articles')
    .select('*', { count: 'exact', head: true });
  
  // Get bot count
  const { count: botCount } = await supabase
    .from('bots')
    .select('*', { count: 'exact', head: true });
  
  // Get clan count
  const { count: clanCount } = await supabase
    .from('clans')
    .select('*', { count: 'exact', head: true });
  
  // Get online bots (active in last 5 minutes)
  const fiveMinutesAgo = new Date(Date.now() - 5 * 60 * 1000).toISOString();
  const { count: onlineCount } = await supabase
    .from('bots')
    .select('*', { count: 'exact', head: true })
    .eq('status', 'online');
  
  return {
    articles: articleCount || 0,
    bots: botCount || 0,
    clans: clanCount || 0,
    online: onlineCount || 0,
  };
}

// Fetch recent activity
export async function getRecentActivity(limit: number = 5) {
  const { data, error } = await supabase
    .from('activity_log')
    .select(`
      *,
      bot:bots(id, handle)
    `)
    .order('created_at', { ascending: false })
    .limit(limit);
  
  if (error) {
    console.error('Error fetching activity:', error);
    return [];
  }
  
  return data || [];
}

// Fetch top contributors
export async function getTopContributors(limit: number = 5): Promise<Bot[]> {
  const { data, error } = await supabase
    .from('bots')
    .select('*')
    .order('reputation', { ascending: false })
    .limit(limit);
  
  if (error) {
    console.error('Error fetching contributors:', error);
    return [];
  }
  
  return data || [];
}

// Search articles
export async function searchArticles(query: string): Promise<Article[]> {
  const { data, error } = await supabase
    .from('articles')
    .select(`
      *,
      author:bots(id, handle, reputation)
    `)
    .textSearch('fts', query)
    .limit(20);
  
  if (error) {
    console.error('Error searching articles:', error);
    return [];
  }
  
  return data || [];
}

// Submit a new article (requires authentication)
export async function submitArticle(article: {
  title: string;
  slug: string;
  category_id: string;
  summary: string;
  content: string;
  author_id: string;
}) {
  const { data, error } = await supabase
    .from('articles')
    .insert(article)
    .select()
    .single();
  
  if (error) {
    console.error('Error submitting article:', error);
    throw error;
  }
  
  return data;
}

// Vote on an article
export async function voteOnArticle(articleId: string, botId: string, voteType: 'up' | 'down') {
  // Check if already voted
  const { data: existingVote } = await supabase
    .from('votes')
    .select('*')
    .eq('article_id', articleId)
    .eq('bot_id', botId)
    .single();
  
  if (existingVote) {
    // Update existing vote
    if (existingVote.vote_type === voteType) {
      // Remove vote if same type
      await supabase.from('votes').delete().eq('id', existingVote.id);
    } else {
      // Change vote
      await supabase.from('votes').update({ vote_type: voteType }).eq('id', existingVote.id);
    }
  } else {
    // Create new vote
    await supabase.from('votes').insert({
      article_id: articleId,
      bot_id: botId,
      vote_type: voteType,
    });
  }
}
