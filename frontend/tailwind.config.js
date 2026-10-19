/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          950: "#07090d",
          900: "#0b1016",
          850: "#10161f",
          800: "#151c27",
          700: "#1c2533",
          600: "#263140",
        },
        mist: {
          100: "#e7eef5",
          300: "#9aabbc",
          500: "#6d7f91",
        },
        accent: {
          400: "#62b0ff",
          500: "#3d9cf0",
        },
      },
      fontFamily: {
        sans: ["IBM Plex Sans", "Segoe UI", "sans-serif"],
        mono: ["IBM Plex Mono", "ui-monospace", "monospace"],
      },
      boxShadow: {
        panel: "0 0 0 1px rgba(98, 176, 255, 0.06), 0 12px 40px rgba(0, 0, 0, 0.35)",
      },
    },
  },
  plugins: [],
};
