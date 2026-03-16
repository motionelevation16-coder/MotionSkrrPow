/**
 * Motion Elevation — Funnel Analytics Tracking Snippet
 * =====================================================
 * Paste this into your website's <head> or before </body>.
 * Works on any HTML page — no frameworks required.
 *
 * SETUP: Replace REPLACE_WITH_YOUR_WEBHOOK_URL below with the
 * webhook URL from your n8n workflow 06-funnel-analytics-tracker.
 *
 * Version: 1.0.0
 */

(function () {
  'use strict';

  // ======================================================
  // CONFIG — REPLACE THIS VALUE
  // ======================================================
  const WEBHOOK_URL = 'REPLACE_WITH_YOUR_WEBHOOK_URL';
  // ======================================================

  // Generate or restore a session ID (persists per browser session)
  const SESSION_ID = sessionStorage.getItem('me_session_id') || (() => {
    const id = 'ses_' + Math.random().toString(36).substr(2, 12) + '_' + Date.now();
    sessionStorage.setItem('me_session_id', id);
    return id;
  })();

  // Parse UTM params from URL
  const urlParams = new URLSearchParams(window.location.search);
  const UTM = {
    utmSource: urlParams.get('utm_source') || sessionStorage.getItem('me_utm_source') || '',
    utmMedium: urlParams.get('utm_medium') || sessionStorage.getItem('me_utm_medium') || '',
    utmCampaign: urlParams.get('utm_campaign') || sessionStorage.getItem('me_utm_campaign') || ''
  };
  // Persist UTMs for the session
  if (UTM.utmSource) sessionStorage.setItem('me_utm_source', UTM.utmSource);
  if (UTM.utmMedium) sessionStorage.setItem('me_utm_medium', UTM.utmMedium);
  if (UTM.utmCampaign) sessionStorage.setItem('me_utm_campaign', UTM.utmCampaign);

  // Page entry timestamp
  const PAGE_START = Date.now();

  /**
   * Core tracking function — sends event to n8n webhook
   * @param {string} eventType - Type of event (page_view, scroll_depth, button_click, etc.)
   * @param {Object} extraData - Additional data to include
   */
  function track(eventType, extraData = {}) {
    const payload = {
      sessionId: SESSION_ID,
      pageUrl: window.location.href,
      pageTitle: document.title,
      eventType: eventType,
      timeOnPage: Math.round((Date.now() - PAGE_START) / 1000),
      userAgent: navigator.userAgent,
      referrer: document.referrer,
      ...UTM,
      ...extraData
    };

    // Use sendBeacon for reliability (especially on page unload)
    if (navigator.sendBeacon) {
      const blob = new Blob([JSON.stringify(payload)], { type: 'application/json' });
      navigator.sendBeacon(WEBHOOK_URL, blob);
    } else {
      // Fallback to fetch
      fetch(WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        keepalive: true
      }).catch(() => {}); // Silent fail — don't break the page
    }
  }

  // ======================================================
  // 1. PAGE VIEW — fires on load
  // ======================================================
  track('page_view');

  // ======================================================
  // 2. SCROLL DEPTH — tracks 25%, 50%, 75%, 100%
  // ======================================================
  const scrollMilestones = [25, 50, 75, 100];
  const scrollFired = new Set();

  function onScroll() {
    const scrolled = window.scrollY + window.innerHeight;
    const total = document.documentElement.scrollHeight;
    const pct = Math.round((scrolled / total) * 100);

    for (const milestone of scrollMilestones) {
      if (pct >= milestone && !scrollFired.has(milestone)) {
        scrollFired.add(milestone);
        track('scroll_depth', { scrollDepth: milestone, eventValue: milestone + '%' });
      }
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });

  // ======================================================
  // 3. TIME MILESTONES — 30s, 60s, 120s on page
  // ======================================================
  const timeMilestones = [30, 60, 120];
  timeMilestones.forEach(seconds => {
    setTimeout(() => {
      track('time_milestone', { eventValue: seconds + 's', timeOnPage: seconds });
    }, seconds * 1000);
  });

  // ======================================================
  // 4. BUTTON / CTA CLICKS — tracks any element with data-track attribute
  //
  // Usage: <button data-track="hero-cta">Sign Up</button>
  //        <a data-track="pricing-link" href="/pricing">Pricing</a>
  // ======================================================
  document.addEventListener('click', function (e) {
    const target = e.target.closest('[data-track]');
    if (target) {
      const trackId = target.getAttribute('data-track');
      const trackLabel = target.getAttribute('data-track-label') || target.innerText?.trim().slice(0, 50) || '';
      track('button_click', { buttonId: trackId, eventValue: trackLabel });
    }
  });

  // ======================================================
  // 5. QUIZ / MULTI-STEP FORM PROGRESS
  //
  // Usage: Call window.meTrackQuizStep('step-name') from your quiz JS
  //        e.g. window.meTrackQuizStep('step-2-budget')
  // ======================================================
  window.meTrackQuizStep = function (stepName, stepData = {}) {
    track('quiz_step', { quizStep: stepName, eventValue: stepName, ...stepData });
  };

  // ======================================================
  // 6. CUSTOM EVENT — call from anywhere on the page
  //
  // Usage: window.meTrack('video_play', { eventValue: 'hero-video' })
  // ======================================================
  window.meTrack = function (eventType, data = {}) {
    track(eventType, data);
  };

  // ======================================================
  // 7. EXIT INTENT — fires when mouse leaves the viewport
  // ======================================================
  let exitFired = false;
  document.addEventListener('mouseleave', function (e) {
    if (e.clientY < 0 && !exitFired) {
      exitFired = true;
      track('exit_intent', { scrollDepth: Math.max(...scrollFired, 0) });
    }
  });

  // ======================================================
  // 8. PAGE UNLOAD — sends final time-on-page
  // ======================================================
  window.addEventListener('beforeunload', function () {
    track('page_exit', {
      timeOnPage: Math.round((Date.now() - PAGE_START) / 1000),
      scrollDepth: Math.max(...scrollFired, 0)
    });
  });

  // Debug mode — set localStorage.setItem('me_debug', '1') in console to see events
  if (localStorage.getItem('me_debug') === '1') {
    const originalTrack = track;
    window._meTrackDebug = originalTrack;
    console.log('[MotionElevation] Tracking snippet loaded. Session:', SESSION_ID);
  }

})();

/*
 * ============================================================
 * QUICK START GUIDE
 * ============================================================
 *
 * 1. Paste this script into every page you want to track
 *    (or add to your site's global header/footer template)
 *
 * 2. Replace REPLACE_WITH_YOUR_WEBHOOK_URL with the URL
 *    from your n8n workflow 06 webhook node
 *
 * 3. To track specific buttons, add data-track="button-name" to them:
 *    <button data-track="hero-cta">Get Started</button>
 *
 * 4. To track quiz steps, call from your quiz JS:
 *    window.meTrackQuizStep('step-2-niche-selection')
 *
 * 5. For custom events anywhere on the page:
 *    window.meTrack('video_play', { eventValue: 'testimonial-video' })
 *
 * 6. Debug mode (open browser console, then type):
 *    localStorage.setItem('me_debug', '1'); location.reload();
 *
 * EVENTS SENT AUTOMATICALLY:
 *   - page_view     — on every page load
 *   - scroll_depth  — at 25%, 50%, 75%, 100% scroll
 *   - time_milestone — at 30s, 60s, 120s on page
 *   - button_click  — on [data-track] elements
 *   - exit_intent   — on mouse leave (desktop only)
 *   - page_exit     — on page close/navigate away
 *
 * NO COOKIES REQUIRED. No third-party dependencies.
 * Data goes directly to your n8n instance. 100% yours.
 * ============================================================
 */
