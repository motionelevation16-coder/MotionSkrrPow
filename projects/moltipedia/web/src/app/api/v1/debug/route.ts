import { NextResponse } from 'next/server';

export async function GET() {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  
  return NextResponse.json({
    hasUrl: !!supabaseUrl,
    urlPrefix: supabaseUrl ? supabaseUrl.substring(0, 30) + '...' : 'NOT SET',
    hasKey: !!supabaseKey,
    keyPrefix: supabaseKey ? supabaseKey.substring(0, 20) + '...' : 'NOT SET',
  });
}
