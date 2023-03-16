const colors = require("tailwindcss/colors");

// Removing deprecated colors to avoid warning messages
delete colors["lightBlue"];
delete colors["warmGray"];
delete colors["trueGray"];
delete colors["coolGray"];
delete colors["blueGray"];

/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: "jit",
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    colors: {
      ...colors,
      primary: "#ef5da8",
      "primary-dark": "#bd4a85",
    },
  },
  plugins: [],
};
