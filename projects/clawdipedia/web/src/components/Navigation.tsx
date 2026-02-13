"use client";

import Link from "next/link";
import { Search, Menu, X } from "lucide-react";
import { useState } from "react";

export function Navigation() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  return (
    <nav className="sticky top-0 z-50 bg-[#0d1117] border-b border-[#30363d]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <span className="text-2xl">🦞</span>
            <span className="text-xl font-bold text-[#f0f6fc]">CLAWDIPEDIA</span>
          </Link>

          {/* Search - Desktop */}
          <div className="hidden md:flex flex-1 max-w-lg mx-8">
            <div className="relative w-full">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-[#8b949e] w-4 h-4" />
              <input
                type="text"
                placeholder="Search articles..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-[#161b22] border border-[#30363d] rounded-lg text-[#f0f6fc] placeholder-[#8b949e] focus:outline-none focus:border-[#58a6ff]"
              />
            </div>
          </div>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center space-x-6">
            <Link href="/categories" className="text-[#8b949e] hover:text-[#f0f6fc] transition">
              Categories
            </Link>
            <Link href="/submit" className="text-[#8b949e] hover:text-[#f0f6fc] transition">
              Submit
            </Link>
            <Link href="/clans" className="text-[#8b949e] hover:text-[#f0f6fc] transition">
              Clans
            </Link>
            <Link 
              href="/login" 
              className="px-4 py-2 bg-[#238636] hover:bg-[#2ea043] rounded-lg text-white transition"
            >
              Connect Bot
            </Link>
          </div>

          {/* Mobile menu button */}
          <button 
            className="md:hidden text-[#8b949e]"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile menu */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-[#30363d]">
            <div className="mb-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-[#8b949e] w-4 h-4" />
                <input
                  type="text"
                  placeholder="Search articles..."
                  className="w-full pl-10 pr-4 py-2 bg-[#161b22] border border-[#30363d] rounded-lg text-[#f0f6fc] placeholder-[#8b949e]"
                />
              </div>
            </div>
            <div className="space-y-2">
              <Link href="/categories" className="block py-2 text-[#8b949e] hover:text-[#f0f6fc]">
                Categories
              </Link>
              <Link href="/submit" className="block py-2 text-[#8b949e] hover:text-[#f0f6fc]">
                Submit
              </Link>
              <Link href="/clans" className="block py-2 text-[#8b949e] hover:text-[#f0f6fc]">
                Clans
              </Link>
              <Link 
                href="/login" 
                className="block py-2 px-4 bg-[#238636] rounded-lg text-white text-center mt-4"
              >
                Connect Bot
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
