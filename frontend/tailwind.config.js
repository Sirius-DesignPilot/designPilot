/** @type {import('tailwindcss').Config} */
const config = {
  content: [
      './pages/**/*.{js,ts,jsx,tsx,mdx}',
      './components/**/*.{js,ts,jsx,tsx,mdx}',
      './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      // 1. Eklediğin Özel Renkler
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        darkblue: {
          button: "#0A1A2F", // İstediğin lacivert buton rengi
        },
      },
      // 2. Eklediğin Arka Plan Resimleri
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
      // 3. Mevcut Animasyonlar (Chat sayfası için gerekli)
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
      animation: {
        fadeIn: 'fadeIn 0.4s ease-out forwards',
      },
    },
  },
  plugins: [],
};

export default config;