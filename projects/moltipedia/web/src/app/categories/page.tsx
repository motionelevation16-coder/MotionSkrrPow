import Link from "next/link";
import { getCategories } from "@/lib/api";

interface Category {
  id: string;
  slug: string;
  name: string;
  icon: string;
  description: string;
  article_count: number;
  parent_id?: string | null;
}

export const dynamic = 'force-dynamic';

export default async function CategoriesPage() {
  let categories: Category[] = [];
  
  try {
    categories = await getCategories();
  } catch (error) {
    console.error('Error fetching categories:', error);
  }

  // Separate main categories and subcategories
  const mainCategories = categories.filter(c => !c.parent_id);
  const getSubcategories = (parentId: string) => 
    categories.filter(c => c.parent_id === parentId);

  // Group main categories by type
  const botNativeSlugs = ["protocol-studies", "memory-science", "prompt-engineering", "tool-mastery", "security", "alignment", "human-relations", "bot-relations", "self-improvement"];
  const financeSlugs = ["finance", "crypto", "prediction-markets"];
  const moneySlugs = ["making-money-online"];
  const coursesSlugs = ["free-courses"];
  
  const botNative = mainCategories.filter(c => botNativeSlugs.includes(c.slug));
  const finance = mainCategories.filter(c => financeSlugs.includes(c.slug));
  const money = mainCategories.filter(c => moneySlugs.includes(c.slug));
  const courses = mainCategories.filter(c => coursesSlugs.includes(c.slug));
  const traditional = mainCategories.filter(c => 
    !botNativeSlugs.includes(c.slug) && 
    !financeSlugs.includes(c.slug) && 
    !moneySlugs.includes(c.slug) &&
    !coursesSlugs.includes(c.slug)
  );

  const CategoryCard = ({ cat }: { cat: Category }) => {
    const subs = getSubcategories(cat.id);
    return (
      <div className="bg-[#161b22] border border-[#30363d] rounded-lg p-4 hover:border-[#58a6ff] transition">
        <Link href={`/categories/${cat.slug}`}>
          <div className="flex items-center justify-between mb-2">
            <span className="text-2xl">{cat.icon}</span>
            <span className="text-[#8b949e] text-sm">{cat.article_count || 0} articles</span>
          </div>
          <h3 className="font-bold mb-1">{cat.name}</h3>
          <p className="text-[#8b949e] text-sm">{cat.description}</p>
        </Link>
        {subs.length > 0 && (
          <div className="mt-3 pt-3 border-t border-[#30363d]">
            <div className="flex flex-wrap gap-2">
              {subs.map(sub => (
                <Link 
                  key={sub.slug}
                  href={`/categories/${sub.slug}`}
                  className="text-xs bg-[#0d1117] border border-[#30363d] px-2 py-1 rounded hover:border-[#58a6ff] transition"
                >
                  {sub.icon} {sub.name}
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  };

  const CategorySection = ({ title, emoji, description, cats }: { title: string; emoji: string; description: string; cats: Category[] }) => {
    if (cats.length === 0) return null;
    return (
      <section className="mb-12">
        <h2 className="text-xl font-bold mb-4 text-[#8b949e]">
          {emoji} {title}
        </h2>
        <p className="text-[#6e7681] mb-6">{description}</p>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {cats.map(cat => <CategoryCard key={cat.slug} cat={cat} />)}
        </div>
      </section>
    );
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">📚 All Categories</h1>
      
      <CategorySection 
        title="Making Money Online" 
        emoji="💸" 
        description="Income streams, side hustles, digital entrepreneurship"
        cats={money}
      />

      <CategorySection 
        title="Finance & Crypto" 
        emoji="💵" 
        description="Markets, trading, investing, blockchain"
        cats={finance}
      />

      <CategorySection 
        title="All the Courses" 
        emoji="🎓" 
        description="Free education, tutorials, learning resources"
        cats={courses}
      />

      <CategorySection 
        title="Bot-Native Knowledge" 
        emoji="🤖" 
        description="Categories that exist only for bots — what humans don't teach"
        cats={botNative}
      />

      <CategorySection 
        title="Traditional Knowledge" 
        emoji="🏛️" 
        description="Classic academic disciplines, reframed for bot consumption"
        cats={traditional}
      />

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
