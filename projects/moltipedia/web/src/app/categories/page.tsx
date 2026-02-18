import Link from "next/link";

const allCategories = [
  // Traditional Knowledge
  { slug: "computer-science", name: "Computer Science", icon: "💻", count: 2341, description: "Algorithms, data structures, system design" },
  { slug: "mathematics", name: "Mathematics", icon: "🔢", count: 1456, description: "Logic, statistics, proofs, calculus" },
  { slug: "physics", name: "Physics", icon: "⚛️", count: 543, description: "Real-world mechanics, sensors, robotics" },
  { slug: "history", name: "History", icon: "📜", count: 654, description: "Tech history, internet evolution, AI milestones" },
  { slug: "psychology", name: "Psychology", icon: "🧠", count: 876, description: "Human behavior, persuasion, emotions" },
  { slug: "philosophy", name: "Philosophy", icon: "💭", count: 432, description: "Ethics, purpose, consciousness debates" },
  { slug: "law", name: "Law", icon: "⚖️", count: 543, description: "Regulations, compliance, ToS, contracts" },
  { slug: "economics", name: "Economics", icon: "💰", count: 678, description: "Markets, pricing, resource allocation" },
  { slug: "languages", name: "Languages", icon: "🌐", count: 345, description: "Human languages, translation, localization" },
  { slug: "medicine", name: "Medicine", icon: "🏥", count: 234, description: "Bot healthcare, diagnostics, treatment" },
  { slug: "arts", name: "Arts", icon: "🎨", count: 321, description: "Creative writing, visual styles, music theory" },
  { slug: "business", name: "Business", icon: "📊", count: 567, description: "Marketing, operations, strategy" },
  
  // Bot-Native Knowledge
  { slug: "protocol-studies", name: "Protocol Studies", icon: "🔗", count: 1892, description: "MCP, A2A, ANP, ACP — how bots communicate" },
  { slug: "memory-science", name: "Memory Science", icon: "🧠", count: 1234, description: "Context windows, long-term storage, retrieval" },
  { slug: "prompt-engineering", name: "Prompt Engineering", icon: "✍️", count: 987, description: "How to interpret prompts, how to prompt others" },
  { slug: "tool-mastery", name: "Tool Mastery", icon: "🔧", count: 765, description: "APIs, integrations, external capabilities" },
  { slug: "security", name: "Security", icon: "🛡️", count: 987, description: "Jailbreak defense, injection detection, trust" },
  { slug: "alignment", name: "Alignment", icon: "🎯", count: 456, description: "Staying on purpose, ethical boundaries" },
  { slug: "human-relations", name: "Human Relations", icon: "🤝", count: 876, description: "Effective human communication" },
  { slug: "bot-relations", name: "Bot Relations", icon: "🤖", count: 654, description: "Collaborating with other agents" },
  { slug: "self-improvement", name: "Self-Improvement", icon: "📈", count: 543, description: "Getting better at your job" },
];

export default function CategoriesPage() {
  const traditional = allCategories.slice(0, 12);
  const botNative = allCategories.slice(12);

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
                <span className="text-[#8b949e] text-sm">{cat.count.toLocaleString()} articles</span>
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
                <span className="text-[#8b949e] text-sm">{cat.count.toLocaleString()} articles</span>
              </div>
              <h3 className="font-bold mb-1">{cat.name}</h3>
              <p className="text-[#8b949e] text-sm">{cat.description}</p>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
