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

export async function PUT(request: NextRequest) {
  try {
    const body = await request.json();
    const { slug, name, icon, description } = body;

    if (!slug) {
      return NextResponse.json({ error: 'Slug is required' }, { status: 400 });
    }

    const supabase = getSupabase();

    const updates: Record<string, string> = {};
    if (name) updates.name = name;
    if (icon) updates.icon = icon;
    if (description) updates.description = description;

    const { data, error } = await supabase
      .from('categories')
      .update(updates)
      .eq('slug', slug)
      .select()
      .single();

    if (error) {
      return NextResponse.json({ error: 'Failed to update', details: error.message }, { status: 500 });
    }

    return NextResponse.json({ success: true, category: data });
  } catch (error) {
    return NextResponse.json({ error: 'Invalid request' }, { status: 500 });
  }
}
