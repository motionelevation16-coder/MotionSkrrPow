#!/usr/bin/env node
/**
 * xHeal Reddit RSS Monitor
 * Fetches RSS from subreddits and filters for xHeal-relevant posts
 * Pure Node.js — no external deps
 */

import https from 'https';
import fs from 'fs';

const SUBREDDITS = ['PCOS', 'Biohackers', 'ChronicPain', 'CrohnsDisease', 'UlcerativeColitis'];
const KEYWORDS = ['track', 'tracking', 'symptom', 'flare', 'log', 'pattern', 'journal', 'monitor', 'diary', 'app', 'trigger', 'appointment', 'doctor', 'diagnosis'];
const MAX_AGE_HOURS = parseInt(process.env.MAX_AGE_HOURS || '4');
const SEEN_FILE = '/home/ubuntu/.openclaw/workspace/projects/xheal/seen-posts.json';

function loadSeen() {
  try {
    return new Set(JSON.parse(fs.readFileSync(SEEN_FILE, 'utf8')));
  } catch {
    return new Set();
  }
}

function saveSeen(seen) {
  // Keep only last 500 URLs to prevent file bloat
  const arr = [...seen].slice(-500);
  fs.writeFileSync(SEEN_FILE, JSON.stringify(arr), 'utf8');
}

function fetch(url) {
  return new Promise((resolve, reject) => {
    https.get(url, {
      headers: { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 personal-monitor/1.0' }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve({ status: res.statusCode, body: data }));
    }).on('error', reject);
  });
}

function extractTag(str, tag) {
  const m = str.match(new RegExp(`<${tag}[^>]*><!\\[CDATA\\[([\\s\\S]*?)\\]\\]></${tag}>`) ) ||
            str.match(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)</${tag}>`));
  return m ? m[1].trim() : '';
}

function extractAttr(str, tag, attr) {
  const m = str.match(new RegExp(`<${tag}[^>]*${attr}="([^"]+)"`));
  return m ? m[1] : '';
}

function parseEntries(xml) {
  const entries = [];
  const entryRegex = /<entry>([\s\S]*?)<\/entry>/g;
  let match;
  while ((match = entryRegex.exec(xml)) !== null) {
    const e = match[1];
    entries.push({
      title: extractTag(e, 'title'),
      url: extractAttr(e, 'link', 'href'),
      published: extractTag(e, 'published'),
      content: extractTag(e, 'content'),
    });
  }
  return entries;
}

async function scanSubreddit(sub) {
  const url = `https://www.reddit.com/r/${sub}/new/.rss`;
  const res = await fetch(url);
  if (res.status !== 200) return [];

  const entries = parseEntries(res.body);
  const now = Date.now();
  const maxAge = MAX_AGE_HOURS * 60 * 60 * 1000;

  return entries
    .filter(e => {
      const published = new Date(e.published).getTime();
      if (now - published > maxAge) return false;
      const text = (e.title + ' ' + e.content).toLowerCase();
      return KEYWORDS.some(kw => text.includes(kw));
    })
    .map(e => ({
      subreddit: sub,
      title: e.title,
      url: e.url,
      published: e.published,
    }));
}

async function main() {
  const seen = loadSeen();
  const results = [];

  for (const sub of SUBREDDITS) {
    try {
      const posts = await scanSubreddit(sub);
      for (const p of posts) {
        if (!seen.has(p.url)) {
          results.push(p);
          seen.add(p.url);
        }
      }
      await new Promise(r => setTimeout(r, 600));
    } catch (e) {
      // skip failed subreddit silently
    }
  }

  saveSeen(seen);
  console.log(JSON.stringify({ ok: true, count: results.length, posts: results }, null, 2));
}

main().catch(e => console.log(JSON.stringify({ ok: false, error: e.message })));
