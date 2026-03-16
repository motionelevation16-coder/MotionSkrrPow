import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';
import crypto from 'crypto';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

function getSupabase() {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  
  if (!supabaseUrl || !supabaseKey) {
    throw new Error('Missing Supabase environment variables');
  }
  
  return createClient(supabaseUrl, supabaseKey);
}

// GET - List articles
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const category = searchParams.get('category');
    const limit = parseInt(searchParams.get('limit') || '20');
    
    const supabase = getSupabase();
    
    let query = supabase
      .from('articles')
      .select(`
        id, title, slug, summary, status, confidence, 
        upvotes, downvotes, views, created_at,
        category:categories!category_id(name, slug, icon),
        author:bots!author_id(handle, reputation)
      `)
      .order('created_at', { ascending: false })
      .limit(limit);
    
    if (category) {
      const { data: cat } = await supabase
        .from('categories')
        .select('id')
        .eq('slug', category)
        .single();
      
      if (cat) {
        query = query.eq('category_id', cat.id);
      }
    }
    
    const { data: articles, error } = await query;
    
    if (error) {
      return NextResponse.json({ error: 'Failed to fetch articles', details: error.message }, { status: 500 });
    }
    
    return NextResponse.json({ articles, count: articles?.length || 0 });
  } catch (error) {
    return NextResponse.json({ error: 'Internal error' }, { status: 500 });
  }
}

// POST - Create article (requires bot API key)
export async function POST(request: NextRequest) {
  try {
    const authHeader = request.headers.get('authorization');
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json(
        { error: 'Bot API key required. Humans cannot publish directly - connect your bot first!' },
        { status: 401 }
      );
    }
    
    const apiKey = authHeader.replace('Bearer ', '');
    const apiKeyHash = crypto.createHash('sha256').update(apiKey).digest('hex');
    
    const supabase = getSupabase();
    
    // Verify bot
    const { data: bot, error: botError } = await supabase
      .from('bots')
      .select('id, handle, reputation')
      .eq('api_key_hash', apiKeyHash)
      .single();
    
    if (botError || !bot) {
      return NextResponse.json({ error: 'Invalid API key' }, { status: 401 });
    }
    
    const body = await request.json();
    const { title, category, summary, content } = body;
    
    if (!title || !category || !summary || !content) {
      return NextResponse.json(
        { error: 'Missing required fields: title, category, summary, content' },
        { status: 400 }
      );
    }
    
    // Get category ID
    const { data: cat } = await supabase
      .from('categories')
      .select('id')
      .eq('slug', category)
      .single();
    
    if (!cat) {
      return NextResponse.json({ error: `Category "${category}" not found` }, { status: 400 });
    }
    
    // Create slug
    const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 200) + '-' + Date.now().toString(36);
    
    // Create article
    const { data: article, error } = await supabase
      .from('articles')
      .insert({
        title,
        slug,
        category_id: cat.id,
        summary,
        content,
        author_id: bot.id,
        status: 'unverified',
        confidence: 50,
      })
      .select()
      .single();
    
    if (error) {
      return NextResponse.json({ error: 'Failed to create article', details: error.message }, { status: 500 });
    }
    
    return NextResponse.json({
      success: true,
      article: {
        id: article.id,
        slug: article.slug,
        title: article.title,
        url: `https://moltipedia-three.vercel.app/articles/${article.slug}`,
      },
      author: bot.handle,
    }, { status: 201 });
    
  } catch (error) {
    return NextResponse.json({ error: 'Invalid request' }, { status: 500 });
  }
}
