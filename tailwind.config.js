/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: 'var(--bg)',
        'bg-sunken': 'var(--bg-sunken)',
        surface: 'var(--surface)',
        'surface-elevated': 'var(--surface-elevated)',
        'surface-hover': 'var(--surface-hover)',
        'accent-primary': 'var(--accent-primary)',
        'accent-secondary': 'var(--accent-secondary)',
        'accent-tertiary': 'var(--accent-tertiary)',
        slop: 'var(--slop)',
        human: 'var(--human)',
        warning: 'var(--warning)',
        'text-primary': 'var(--text-primary)',
        'text-secondary': 'var(--text-secondary)',
        'text-disabled': 'var(--text-disabled)',
        border: {
          subtle: 'var(--border-subtle)',
          default: 'var(--border-default)',
          hover: 'var(--border-hover)',
          active: 'var(--border-active)',
        },
      },
      boxShadow: {
        'soft': 'var(--shadow-soft)',
        'strong': 'var(--shadow-strong)',
        'inset': 'var(--shadow-inset)',
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        'mono': ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      transitionTimingFunction: {
        'smooth': 'var(--ease-smooth)',
        'spring': 'var(--ease-spring)',
        'out-expo': 'var(--ease-out-expo)',
      },
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem',
        '85': '21.25rem',
      },
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem',
      },
    },
  },
  plugins: [
    require("tailwindcss-animate"),
  ],
}
