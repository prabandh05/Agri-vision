// AgriVision — Dark Agricultural Theme
export const Colors = {
  // Background hierarchy
  background:   '#0D1B0F',  // Deep forest green-black
  surface:      '#152217',  // Card surface
  surfaceHigh:  '#1E3022',  // Elevated surfaces
  surfaceBorder:'#2A4030',  // Card borders

  // Brand greens
  primary:      '#4CAF6F',  // Vibrant leaf green
  primaryLight: '#6FCF8E',  // Light accent
  primaryDark:  '#2E7D4F',  // Pressed state
  primaryGlow:  'rgba(76, 175, 111, 0.15)',

  // Accent / Alert colors
  accent:       '#F9A825',  // Harvest gold
  accentLight:  '#FFD54F',
  danger:       '#EF5350',  // Disease / alert red
  dangerLight:  '#FF8A80',
  warning:      '#FF7043',  // Pest warning orange
  info:         '#42A5F5',  // Info blue
  organic:      '#8BC34A',  // Organic farming
  water:        '#29B6F6',  // Irrigation/water

  // Text
  textPrimary:  '#E8F5E9',  // Main text — near white with green tint
  textSecondary:'#A5D6A7',  // Secondary text
  textMuted:    '#5C8A62',  // Muted text
  textDark:     '#0D1B0F',  // Text on light backgrounds

  // Chat
  userBubble:   '#1B5E20',  // User message bubble
  aiBubble:     '#1E3022',  // AI response bubble
  userText:     '#C8E6C9',
  aiText:       '#E8F5E9',

  // Tab bar
  tabActive:    '#4CAF6F',
  tabInactive:  '#5C8A62',
  tabBackground:'#0D1B0F',
};

export const Fonts = {
  sizes: {
    xs:   11,
    sm:   13,
    md:   15,
    lg:   17,
    xl:   20,
    xxl:  24,
    xxxl: 30,
  },
  weights: {
    regular: '400',
    medium:  '500',
    semibold:'600',
    bold:    '700',
  },
};

export const Spacing = {
  xs:  4,
  sm:  8,
  md:  12,
  lg:  16,
  xl:  20,
  xxl: 28,
  xxxl:36,
};

export const Radius = {
  sm:   8,
  md:   12,
  lg:   16,
  xl:   20,
  full: 999,
};

export const Shadow = {
  card: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 6,
    elevation: 4,
  },
  glow: {
    shadowColor: '#4CAF6F',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.4,
    shadowRadius: 8,
    elevation: 6,
  },
};

export const CategoryMeta = {
  disease:    { emoji: '🔴', label: 'Diseases & Pests',     color: '#EF5350' },
  fertilizer: { emoji: '🧪', label: 'Fertilizer & Nutrition', color: '#F9A825' },
  irrigation: { emoji: '💧', label: 'Irrigation & Water',   color: '#29B6F6' },
  crop:       { emoji: '🌾', label: 'Crop Info',             color: '#4CAF6F' },
  scheme:     { emoji: '🏛️', label: 'Government Schemes',   color: '#AB47BC' },
  organic:    { emoji: '🌿', label: 'Organic Farming',       color: '#8BC34A' },
  faq:        { emoji: '❓', label: 'General FAQ',           color: '#42A5F5' },
  recommendation: { emoji: '📋', label: 'Recommendations',  color: '#FF7043' },
};
