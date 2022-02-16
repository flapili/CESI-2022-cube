module.exports = {
  plugins: [
    require('@tailwindcss/line-clamp'),
  ],
  content: ["./src/**/*.{html,js,vue}"],
  theme: {
    extend: {
      colors: {
        primary: "#009BA0",
        secondary: "#CAE4E4",
      }
    },
  },
  prefix: "tw-",
}