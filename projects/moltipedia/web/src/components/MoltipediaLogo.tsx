"use client";

export function MoltipediaLogo({ className = "" }: { className?: string }) {
  return (
    <span className={`font-bold text-[#c0392b] ${className}`}>
      {/* M with claw styling */}
      <span className="relative inline-block">
        <span className="relative">
          M
          {/* Left claw */}
          <svg 
            className="absolute -top-1 -left-1 w-3 h-3 text-[#c0392b]" 
            viewBox="0 0 24 24" 
            fill="currentColor"
          >
            <path d="M4 8 L8 4 L6 8 L10 6 L8 10 L4 8 Z" />
          </svg>
          {/* Right claw */}
          <svg 
            className="absolute -top-1 -right-1 w-3 h-3 text-[#c0392b] transform scale-x-[-1]" 
            viewBox="0 0 24 24" 
            fill="currentColor"
          >
            <path d="M4 8 L8 4 L6 8 L10 6 L8 10 L4 8 Z" />
          </svg>
        </span>
      </span>
      OLTIPEDIA
    </span>
  );
}

// Simple SVG version of the full logo text with claws
export function MoltipediaLogoSVG({ size = 24 }: { size?: number }) {
  return (
    <svg 
      width={size * 8} 
      height={size} 
      viewBox="0 0 200 30" 
      className="text-[#c0392b]"
    >
      {/* Claw shapes on top of M */}
      <path 
        d="M5 8 Q8 2, 12 6 L10 10 Q7 6, 5 8" 
        fill="#c0392b"
      />
      <path 
        d="M25 8 Q22 2, 18 6 L20 10 Q23 6, 25 8" 
        fill="#c0392b"
      />
      {/* MOLTIPEDIA text */}
      <text 
        x="2" 
        y="24" 
        fill="#c0392b" 
        fontFamily="system-ui, sans-serif" 
        fontWeight="bold" 
        fontSize="20"
      >
        MOLTIPEDIA
      </text>
    </svg>
  );
}
