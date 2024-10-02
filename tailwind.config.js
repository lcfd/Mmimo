/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./blog/**/*.{html,js}", "./templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        hint: "#666f75",
        disabled: "#a0a6ac",
        primary: "#16161a",

        body: "#f8f9fa",

        base: "#ffffff",
        baseAlt1: "#e4e9ec",
        baseAlt2: "#d7dde4",
        baseAlt3: "#c6cdd7",
        baseAlt4: "#a5b0c0",

        info: "#5499e8",
        infoAlt: "#cee2f8",

        success: "#32ad84",
        successAlt: "#c4eedc",

        danger: "#e34562",
        dangerAlt: "#f7cad2",

        warning: "#ff944d",
        warningAlt: "#ffd4b8",
      },
    },
    fontFamily: {
      lora: ["Lora Variable"],
    },
  },
  plugins: [],
};
