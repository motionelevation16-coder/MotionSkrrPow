/**
 * demo-data.js — Motion Elevation Client Dashboard
 * Fake data for sales demos (?demo=true mode).
 * Replace with real API/webhook responses in production.
 */

const DEMO_CLIENT = {
  id: "demo-client-001",
  name: "Acme GmbH",
  email: "demo@acme.de",
  token: "demo-token-not-real",
  subscriptionStatus: "active",       // "active" | "inactive" | "trial"
  subscriptionPlan: "Growth",
  subscriptionRenewal: "2026-04-01",
  avatarInitials: "AG",
};

const DEMO_STATS = {
  runsThisMonth: 247,
  emailsSent: 1_840,
  leadsCaptures: 38,
  invoicesSent: 12,
  timeSavedHours: 23,           // hours — the hero gamification number
  timeSavedMinutes: 23 * 60,    // derived
  successRate: 98.4,            // percentage
  mostUsedAutomation: "Email Triage & Auto-Reply",
};

// Status options: "active" | "error" | "running" | "inactive"
const DEMO_AUTOMATIONS = [
  {
    id: "email-triage",
    icon: "📧",
    name: "Email Triage & Auto-Reply",
    description: "Reads incoming emails, categorises them by intent, drafts AI replies for review, and auto-sends low-risk responses.",
    status: "active",
    lastRun: new Date(Date.now() - 1000 * 60 * 14).toISOString(),  // 14 min ago
    runsThisMonth: 89,
    webhookUrl: "https://your-n8n.domain/webhook/email-triage",
    enabled: true,
  },
  {
    id: "lead-crm",
    icon: "🎯",
    name: "Lead Capture & CRM Sync",
    description: "Pulls new leads from forms, LinkedIn, and ads — enriches them and pushes to your CRM with tags and lifecycle stage.",
    status: "active",
    lastRun: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(), // 2h ago
    runsThisMonth: 38,
    webhookUrl: "https://your-n8n.domain/webhook/lead-crm",
    enabled: true,
  },
  {
    id: "invoice-reminder",
    icon: "💶",
    name: "Invoice Reminder Sequence",
    description: "Sends polite payment reminders at 3, 7, and 14 days overdue — escalates to a formal notice if needed.",
    status: "active",
    lastRun: new Date(Date.now() - 1000 * 60 * 60 * 5).toISOString(), // 5h ago
    runsThisMonth: 12,
    webhookUrl: "https://your-n8n.domain/webhook/invoice-reminder",
    enabled: true,
  },
  {
    id: "ai-support",
    icon: "🤖",
    name: "AI Customer Support Chatbot",
    description: "Answers FAQs via your website chat, escalates complex issues to your inbox, and logs every conversation.",
    status: "running",
    lastRun: new Date(Date.now() - 1000 * 30).toISOString(),           // 30s ago (running)
    runsThisMonth: 63,
    webhookUrl: "https://your-n8n.domain/webhook/ai-support",
    enabled: true,
  },
  {
    id: "meeting-booking",
    icon: "📅",
    name: "Meeting Booking & Reminders",
    description: "Sends confirmation emails on booking, reminders 24h and 1h before, and follow-up notes afterwards.",
    status: "active",
    lastRun: new Date(Date.now() - 1000 * 60 * 60 * 8).toISOString(), // 8h ago
    runsThisMonth: 21,
    webhookUrl: "https://your-n8n.domain/webhook/meeting-booking",
    enabled: true,
  },
  {
    id: "funnel-report",
    icon: "📊",
    name: "Weekly Funnel Report",
    description: "Aggregates your leads, conversion rates, and revenue data every Monday — sends a clean PDF to your inbox.",
    status: "active",
    lastRun: new Date(Date.now() - 1000 * 60 * 60 * 24 * 2).toISOString(), // 2d ago
    runsThisMonth: 4,
    webhookUrl: "https://your-n8n.domain/webhook/funnel-report",
    enabled: true,
  },
  {
    id: "social-scheduler",
    icon: "📱",
    name: "Social Media Scheduler",
    description: "Drafts posts from your content calendar, schedules to Instagram / LinkedIn / X at peak hours, and tracks engagement.",
    status: "error",
    lastRun: new Date(Date.now() - 1000 * 60 * 60 * 3).toISOString(), // 3h ago
    runsThisMonth: 14,
    webhookUrl: "https://your-n8n.domain/webhook/social-scheduler",
    enabled: true,
    errorMessage: "Instagram API token expired — reconnect in Settings.",
  },
  {
    id: "ecommerce-flow",
    icon: "🛒",
    name: "E-Commerce Order Flow",
    description: "On new order: sends confirmation, updates inventory, triggers fulfilment, and handles returns/refunds automatically.",
    status: "inactive",
    lastRun: null,
    runsThisMonth: 0,
    webhookUrl: "https://your-n8n.domain/webhook/ecommerce-flow",
    enabled: false,
    disabledReason: "Not activated on your plan — upgrade to enable.",
  },
];

// Export for use in dashboard.html
if (typeof module !== 'undefined') {
  module.exports = { DEMO_CLIENT, DEMO_STATS, DEMO_AUTOMATIONS };
}
