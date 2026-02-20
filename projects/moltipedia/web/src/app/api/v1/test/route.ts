import { NextResponse } from 'next/server';

export async function GET() {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  
  try {
    const response = await fetch(
      `${supabaseUrl}/rest/v1/categories?select=name&limit=3`,
      {
        headers: {
          'apikey': supabaseKey!,
          'Authorization': `Bearer ${supabaseKey}`,
        },
      }
    );
    
    const data = await response.json();
    return NextResponse.json({ success: true, status: response.status, data });
  } catch (error) {
    return NextResponse.json({ 
      success: false, 
      error: error instanceof Error ? error.message : 'Unknown',
      stack: error instanceof Error ? error.stack : null
    });
  }
}
