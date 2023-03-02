const colors = require('tailwindcss/colors')

// Removing deprecated colors to avoid warning messages
delete colors['lightBlue'];
delete colors['warmGray'];
delete colors['trueGray'];
delete colors['coolGray'];
delete colors['blueGray'];

/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    colors: {
      ...colors,
      primary: colors.blue[500],
      "primary-dark": colors.blue[400],
    }
  },
  plugins: [],
};
