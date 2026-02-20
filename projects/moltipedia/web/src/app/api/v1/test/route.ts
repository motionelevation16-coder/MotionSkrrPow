import { NextResponse } from 'next/server';

export async function GET() {
  const supabaseUrl = (process.env.NEXT_PUBLIC_SUPABASE_URL || '').trim();
  const supabaseKey = (process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '').trim();
  
  const fullUrl = `${supabaseUrl}/rest/v1/categories?select=name&limit=3`;
  
  try {
    const response = await fetch(fullUrl, {
      headers: {
        'apikey': supabaseKey,
        'Authorization': `Bearer ${supabaseKey}`,
        'Content-Type': 'application/json',
      },
    });
    
    const data = await response.json();
    return NextResponse.json({ success: true, status: response.status, data, url: fullUrl });
  } catch (error) {
    return NextResponse.json({ 
      success: false, 
      error: error instanceof Error ? error.message : 'Unknown',
      url: fullUrl,
      urlLength: fullUrl.length,
    });
  }
}
