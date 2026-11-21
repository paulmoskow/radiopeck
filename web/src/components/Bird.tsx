type BirdProps = {
  className?: string;
};

/** RadioPeck mascot. Decorative: the play button next to it carries the label. */
export default function Bird({ className }: BirdProps) {
  return (
    <svg
      className={className}
      viewBox="0 0 120 110"
      fill="none"
      stroke="#3A3148"
      strokeWidth={3}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {/* body, head, beak, eye, cheek */}
      <ellipse cx="56" cy="70" rx="36" ry="26" fill="#FFF8F0" />
      <circle cx="84" cy="42" r="19" fill="#FFF8F0" />
      <path d="M102 40 L117 45 L102 50 Z" fill="#F2C6A2" />
      <circle cx="88" cy="38" r="2.6" fill="#3A3148" stroke="none" />
      <circle cx="94" cy="47" r="4" fill="#F3C9B8" stroke="none" />
      {/* headphones: band over the head, cup on the ear */}
      <path d="M76 36 C68 14 98 12 102 32" strokeWidth={3.4} />
      <rect x="69" y="35" width="13" height="18" rx="6.5" fill="#E6B79C" />
      {/* wing, three tail feathers, feet */}
      <path d="M38 66 Q56 52 74 68 Q56 82 38 66Z" fill="#DCD3EA" />
      <path d="M22 64 L6 55 M22 69 L3 68 M22 74 L6 82" />
      <path d="M50 95 V104 M64 95 V104 M46 104 H54 M60 104 H68" />
    </svg>
  );
}
