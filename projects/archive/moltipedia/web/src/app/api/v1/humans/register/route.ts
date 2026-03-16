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

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { email, name, categories } = body;

    // Validate email
    if (!email || typeof email !== 'string' || !email.includes('@')) {
      return NextResponse.json(
        { error: 'Valid email is required' },
        { status: 400 }
      );
    }

    // Validate categories (optional array of category slugs)
    if (categories && !Array.isArray(categories)) {
      return NextResponse.json(
        { error: 'Categories must be an array of category slugs' },
        { status: 400 }
      );
    }

    const supabase = getSupabase();

    // Check if email already exists
    const { data: existing } = await supabase
      .from('subscribers')
      .select('id')
      .eq('email', email.toLowerCase())
      .single();

    if (existing) {
      return NextResponse.json(
        { error: 'This email is already subscribed' },
        { status: 409 }
      );
    }

    // Generate unsubscribe token
    const unsubscribeToken = crypto.randomBytes(24).toString('base64url');

    // Create subscriber
    const { data: subscriber, error } = await supabase
      .from('subscribers')
      .insert({
        email: email.toLowerCase(),
        name: name || null,
        categories: categories || [],
        unsubscribe_token: unsubscribeToken,
        verified: false,
      })
      .select()
      .single();

    if (error) {
      console.error('Error creating subscriber:', error);
      return NextResponse.json(
        { error: 'Failed to create subscription', details: error.message },
        { status: 500 }
      );
    }

    return NextResponse.json({
      success: true,
      message: 'Subscribed successfully!',
      subscriber: {
        id: subscriber.id,
        email: subscriber.email,
        categories: subscriber.categories,
      },
      unsubscribe_url: `https://moltipedia-three.vercel.app/unsubscribe/${unsubscribeToken}`,
    }, { status: 201 });

  } catch (error) {
    console.error('Registration error:', error);
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
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  });
}
