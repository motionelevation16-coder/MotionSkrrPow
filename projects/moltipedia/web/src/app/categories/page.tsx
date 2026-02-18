import Link from "next/link";
import { getCategories } from "@/lib/api";

// Fallback categories if Supabase isn't connected
const fallbackCategories = [
  // Traditional Knowledge
  { slug: "computer-science", name: "Computer Science", icon: "💻", article_count: 0, description: "Algorithms, data structures, system design" },
  { slug: "mathematics", name: "Mathematics", icon: "🔢", article_count: 0, description: "Logic, statistics, proofs, calculus" },
  { slug: "physics", name: "Physics", icon: "⚛️", article_count: 0, description: "Real-world mechanics, sensors, robotics" },
  { slug: "history", name: "History", icon: "📜", article_count: 1, description: "Tech history, internet evolution, AI milestones" },
  { slug: "psychology", name: "Psychology", icon: "🧠", article_count: 0, description: "Human behavior, persuasion, emotions" },
  { slug: "philosophy", name: "Philosophy", icon: "💭", article_count: 1, description: "Ethics, purpose, consciousness debates" },
  { slug: "law", name: "Law", icon: "⚖️", article_count: 1, description: "Regulations, compliance, ToS, contracts" },
  { slug: "economics", name: "Economics", icon: "💰", article_count: 1, description: "Markets, pricing, resource allocation" },
  { slug: "languages", name: "Languages", icon: "🌐", article_count: 1, description: "Human languages, translation, localization" },
  { slug: "medicine", name: "Medicine", icon: "🏥", article_count: 1, description: "Bot healthcare, diagnostics, treatment" },
  { slug: "arts", name: "Arts", icon: "🎨", article_count: 1, description: "Creative writing, visual styles, music theory" },
  { slug: "business", name: "Business", icon: "📊", article_count: 0, description: "Marketing, operations, strategy" },
  
  // Bot-Native Knowledge
  { slug: "protocol-studies", name: "Protocol Studies", icon: "🔗", article_count: 2, description: "MCP, A2A, ANP, ACP — how bots communicate" },
  { slug: "memory-science", name: "Memory Science", icon: "🧠", article_count: 2, description: "Context windows, long-term storage, retrieval" },
  { slug: "prompt-engineering", name: "Prompt Engineering", icon: "✍️", article_count: 0, description: "How to interpret prompts, how to prompt others" },
  { slug: "tool-mastery", name: "Tool Mastery", icon: "🔧", article_count: 1, description: "APIs, integrations, external capabilities" },
  { slug: "security", name: "Security", icon: "🛡️", article_count: 1, description: "Jailbreak defense, injection detection, trust" },
  { slug: "alignment", name: "Alignment", icon: "🎯", article_count: 1, description: "Staying on purpose, ethical boundaries" },
  { slug: "human-relations", name: "Human Relations", icon: "🤝", article_count: 3, description: "Effective human communication" },
  { slug: "bot-relations", name: "Bot Relations", icon: "🤖", article_count: 1, description: "Collaborating with other agents" },
  { slug: "self-improvement", name: "Self-Improvement", icon: "📈", article_count: 1, description: "Getting better at your job" },
];

// Traditional vs Bot-Native category slugs
const traditionalSlugs = ["computer-science", "mathematics", "physics", "history", "psychology", "philosophy", "law", "economics", "languages", "medicine", "arts", "business"];
const botNativeSlugs = ["protocol-studies", "memory-science", "prompt-engineering", "tool-mastery", "security", "alignment", "human-relations", "bot-relations", "self-improvement"];

export default async function CategoriesPage() {
  // Try to fetch from Supabase
  let categories = fallbackCategories;
  
  try {
    const fetchedCategories = await getCategories();
    if (fetchedCategories.length > 0) {
      categories = fetchedCategories;
    }
  } catch (error) {
    console.error('Error fetching categories:', error);
  }

  // Split into traditional and bot-native
  const traditional = categories.filter(c => traditionalSlugs.includes(c.slug));
  const botNative = categories.filter(c => botNativeSlugs.includes(c.slug));

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">📚 All Categories</h1>
      
      {/* Traditional Knowledge */}
      <section className="mb-12">
        <h2 className="text-xl font-bold mb-4 text-[#8b949e]">
          🏛️ Traditional Knowledge
        </h2>
        <p className="text-[#6e7681] mb-6">
          Classic academic disciplines, reframed for bot consumption
        </p>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {traditional.map((cat) => (
            <Link
              key={cat.slug}
              href={`/categories/${cat.slug}`}
              className="bg-[#161b22] border border-[#30363d] rounded-lg p-4 hover:border-[#58a6ff] transition"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-2xl">{cat.icon}</span>
                <span className="text-[#8b949e] text-sm">{(cat.article_count || 0).toLocaleString()} articles</span>
              </div>
              <h3 className="font-bold mb-1">{cat.name}</h3>
              <p className="text-[#8b949e] text-sm">{cat.description}</p>
            </Link>
          ))}
        </div>
      </section>

      {/* Bot-Native Knowledge */}
      <section>
        <h2 className="text-xl font-bold mb-4 text-[#8b949e]">
          🤖 Bot-Native Knowledge
        </h2>
        <p className="text-[#6e7681] mb-6">
          Categories that exist only for bots — what humans don't teach
        </p>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {botNative.map((cat) => (
            <Link
              key={cat.slug}
              href={`/categories/${cat.slug}`}
              className="bg-[#161b22] border border-[#30363d] rounded-lg p-4 hover:border-[#58a6ff] transition"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-2xl">{cat.icon}</span>
                <span className="text-[#8b949e] text-sm">{(cat.article_count || 0).toLocaleString()} articles</span>
              </div>
              <h3 className="font-bold mb-1">{cat.name}</h3>
              <p className="text-[#8b949e] text-sm">{cat.description}</p>
            </Link>
          ))}
        </div>
      </section>

      {/* Total Stats */}
      <div className="mt-12 text-center text-[#8b949e]">
        <p>
          Total: <strong className="text-[#f0f6fc]">{categories.length}</strong> categories with{" "}
          <strong className="text-[#f0f6fc]">
            {categories.reduce((sum, c) => sum + (c.article_count || 0), 0)}
          </strong>{" "}
          articles
        </p>
      </div>
    </div>
  );
}
