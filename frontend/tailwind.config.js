/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        display: ['"Geist"', 'system-ui', 'sans-serif'],
        body: ['"Geist"', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
      colors: {
        brand: {
          50:  '#eef9ff',
          100: '#d9f1ff',
          200: '#bbe5ff',
          300: '#8cd4ff',
          400: '#56baff',
          500: '#2e9aff',
          600: '#147af5',
          700: '#0d62e1',
          800: '#114fb6',
          900: '#14448f',
          950: '#112b57',
        },
        canvas: '#0a0a0c',
        tile: {
          DEFAULT: '#141417',
          2: '#1b1b1f',
          3: '#232328',
        },
        line: {
          DEFAULT: '#26262c',
          strong: '#36363d',
        },
        ink: {
          DEFAULT: '#f5f5f7',
          muted: '#c8c8d0',
          subtle: '#8e8e99',
          faint: '#5d5d66',
        },
        pop: {
          mint: '#8fe3a0',
          aqua: '#7de3e8',
          sun: '#f6d66f',
          pink: '#f27aa2',
          coral: '#f58a7a',
        },
      },
      borderRadius: {
        tile: '22px',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease forwards',
        rise: 'rise 0.6s cubic-bezier(0.16, 1, 0.3, 1) both',
        'key-press': 'keyPress 4.8s cubic-bezier(0.16, 1, 0.3, 1) infinite',
        'spin-slow': 'spin 40s linear infinite',
        breathe: 'breathe 2.4s ease-in-out infinite',
        'drawer-in': 'drawerIn 0.35s cubic-bezier(0.16, 1, 0.3, 1) both',
        blink: 'blink 1.2s steps(1, end) infinite',
        shimmer: 'shimmer 1.8s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: { from: { opacity: 0 }, to: { opacity: 1 } },
        rise: { from: { opacity: 0, transform: 'translateY(14px)' }, to: { opacity: 1, transform: 'translateY(0)' } },
        keyPress: {
          '0%, 14%, 100%': { transform: 'translateY(0)', boxShadow: '0 10px 0 var(--k)' },
          '6%': { transform: 'translateY(7px)', boxShadow: '0 3px 0 var(--k)' },
        },
        breathe: { '0%, 100%': { opacity: 1, transform: 'scale(1)' }, '50%': { opacity: 0.45, transform: 'scale(0.8)' } },
        drawerIn: { from: { transform: 'translateX(-100%)' }, to: { transform: 'translateX(0)' } },
        blink: { '0%, 55%': { opacity: 1 }, '56%, 100%': { opacity: 0 } },
        shimmer: { '0%': { transform: 'translateX(-100%)' }, '100%': { transform: 'translateX(300%)' } },
      },
    },
  },
  plugins: [],
}
