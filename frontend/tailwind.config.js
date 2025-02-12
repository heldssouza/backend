/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui')
  ],
  daisyui: {
    themes: [
      {
        light: {
          ...require('daisyui/src/theming/themes')['light'],
          primary: '#4F46E5',
          secondary: '#3B82F6',
          accent: '#10B981',
          neutral: '#374151',
          'base-100': '#F3F4F6',
          'base-200': '#E5E7EB',
          'base-300': '#D1D5DB',
          'base-content': '#1F2937',
        },
        dark: {
          ...require('daisyui/src/theming/themes')['dark'],
          primary: '#4F46E5',
          secondary: '#3B82F6',
          accent: '#10B981',
        },
      },
    ],
  },
}
