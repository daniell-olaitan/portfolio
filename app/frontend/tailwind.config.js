/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js"
  ],
  theme: {
    extend: {
      width: {
        'max-content': 'max-content',
      },
      backgroundImage: theme => ({
        'custom-gradient': 'linear-gradient(to bottom, #f5f5f5 5%, #ffffff 95%)',
      }),
    },
  },
  plugins: [],
}
