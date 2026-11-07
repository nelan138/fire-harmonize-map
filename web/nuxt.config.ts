// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
   modules: ["@nuxt/ui", "@nuxt/image", "@pinia/nuxt", "@nuxtjs/leaflet"],
   css: ["~/assets/css/main.css"],
   compatibilityDate: "2025-07-15",
   devtools: { enabled: false },
   routeRules: {
      "/": { redirect: "/map" },
   },
});
