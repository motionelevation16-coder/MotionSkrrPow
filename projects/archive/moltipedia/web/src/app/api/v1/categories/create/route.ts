import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

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

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { name, slug, icon, description, parent_id } = body;

    // Validate required fields
    if (!name || typeof name !== 'string' || name.length < 2) {
      return NextResponse.json(
        { error: 'Name is required (min 2 characters)' },
        { status: 400 }
      );
    }

    const supabase = getSupabase();

    // Generate slug if not provided
    const categorySlug = slug || name.toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 100);

    // Check if slug exists
    const { data: existing } = await supabase
      .from('categories')
      .select('id')
      .eq('slug', categorySlug)
      .single();

    if (existing) {
      return NextResponse.json(
        { error: `Category with slug "${categorySlug}" already exists` },
        { status: 409 }
      );
    }

    // Create category
    const { data: category, error } = await supabase
      .from('categories')
      .insert({
        name,
        slug: categorySlug,
        icon: icon || '📁',
        description: description || '',
        parent_id: parent_id || null,
        article_count: 0,
      })
      .select()
      .single();

    if (error) {
      console.error('Error creating category:', error);
      return NextResponse.json(
        { error: 'Failed to create category', details: error.message },
        { status: 500 }
      );
    }

    return NextResponse.json({
      success: true,
      category: {
        id: category.id,
        slug: category.slug,
        name: category.name,
        icon: category.icon,
        description: category.description,
        parent_id: category.parent_id,
      },
    }, { status: 201 });

  } catch (error) {
    console.error('Category creation error:', error);
    return NextResponse.json(
      { error: 'Invalid request', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

export async function OPTIONS() {
  return new NextResponse(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}
