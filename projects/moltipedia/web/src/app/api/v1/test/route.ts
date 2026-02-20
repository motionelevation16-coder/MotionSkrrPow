import { NextResponse } from 'next/server';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

export async function GET() {
  const results: Record<string, string> = {};

  // Test 1: Google
  try {
    const r = await fetch('https://www.google.com', { method: 'HEAD' });
    results.google = `OK: ${r.status}`;
  } catch (e) {
    results.google = `FAIL: ${e instanceof Error ? e.message : 'unknown'}`;
  }

  // Test 2: Raw Supabase domain (no path)
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
  try {
    const r = await fetch(supabaseUrl, { method: 'HEAD' });
    results.supabase_root = `OK: ${r.status}`;
  } catch (e) {
    results.supabase_root = `FAIL: ${e instanceof Error ? e.message : 'unknown'}`;
  }

  // Test 3: Different Supabase project (public one)
  try {
    const r = await fetch('https://supabase.com', { method: 'HEAD' });
    results.supabase_main = `OK: ${r.status}`;
  } catch (e) {
    results.supabase_main = `FAIL: ${e instanceof Error ? e.message : 'unknown'}`;
  }

  // Test 4: Another .co domain
  try {
    const r = await fetch('https://vercel.co', { method: 'HEAD' });
    results.vercel_co = `OK: ${r.status}`;
  } catch (e) {
    results.vercel_co = `FAIL: ${e instanceof Error ? e.message : 'unknown'}`;
  }

  return NextResponse.json(results);
}
