import { NextResponse } from 'next/server';

export async function GET() {
  // Test 1: Can we fetch google?
  let googleTest = 'not tested';
  try {
    const r = await fetch('https://www.google.com', { method: 'HEAD' });
    googleTest = `OK: ${r.status}`;
  } catch (e) {
    googleTest = `FAIL: ${e instanceof Error ? e.message : 'unknown'}`;
  }

  // Test 2: Can we fetch Supabase?
  const supabaseUrl = (process.env.NEXT_PUBLIC_SUPABASE_URL || '').trim();
  const supabaseKey = (process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '').trim();
  const fullUrl = `${supabaseUrl}/rest/v1/categories?select=name&limit=1`;
  
  let supabaseTest = 'not tested';
  try {
    const response = await fetch(fullUrl, {
      headers: {
        'apikey': supabaseKey,
        'Authorization': `Bearer ${supabaseKey}`,
      },
    });
    const data = await response.json();
    supabaseTest = `OK: ${response.status} - ${JSON.stringify(data).slice(0, 100)}`;
  } catch (e) {
    supabaseTest = `FAIL: ${e instanceof Error ? e.message : 'unknown'}`;
  }

  return NextResponse.json({ googleTest, supabaseTest, url: fullUrl });
}
