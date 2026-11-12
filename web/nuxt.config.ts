// https://nuxt.com/docs/api/configuration/nuxt-config
import { fileURLToPath } from "node:url";

export default defineNuxtConfig({
   modules: ["@nuxt/ui", "@nuxt/image", "@pinia/nuxt", "@nuxtjs/leaflet"],
   css: ["~/assets/css/main.css"],
   compatibilityDate: "2025-07-15",
   devtools: { enabled: false },
   runtimeConfig: {
      fireDataDir: "public/data",
   },
   nitro: {
      serverAssets: [{ baseName: "sql", dir: fileURLToPath(new URL("./server/sql", import.meta.url)) }],
   },
   routeRules: {
      "/": { redirect: "/map" },
   },
});
