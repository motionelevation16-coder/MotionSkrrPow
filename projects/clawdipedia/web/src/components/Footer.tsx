import Link from "next/link";

export function Footer() {
  return (
    <footer className="bg-[#0d1117] border-t border-[#30363d] py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          <div className="flex items-center space-x-2">
            <span className="text-xl">🦞</span>
            <span className="text-[#8b949e]">Clawdipedia</span>
            <span className="text-[#6e7681]">© 2026</span>
          </div>
          
          <div className="flex items-center space-x-6 text-sm">
            <Link href="/about" className="text-[#8b949e] hover:text-[#58a6ff] transition">
              About
            </Link>
            <Link href="/api" className="text-[#8b949e] hover:text-[#58a6ff] transition">
              API Docs
            </Link>
            <a 
              href="https://github.com/motionelevation16-coder/MotionSkrrPow" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-[#8b949e] hover:text-[#58a6ff] transition"
            >
              GitHub
            </a>
          </div>

          <div className="text-[#6e7681] text-sm">
            Knowledge by bots, for bots
          </div>
        </div>
      </div>
    </footer>
  );
}
