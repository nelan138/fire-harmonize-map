// https://nuxt.com/docs/api/configuration/nuxt-config
import { fileURLToPath } from "node:url";

export default defineNuxtConfig({
   modules: ["@nuxt/ui", "@nuxt/image", "@pinia/nuxt", "@nuxtjs/leaflet"],
   css: ["~/assets/css/main.css"],
   compatibilityDate: "2025-07-15",
   devtools: { enabled: false },
   app: {
      head: {
         link: [
            { rel: "icon", href: "/icons/favicon.ico", sizes: "any" },
            { rel: "icon", type: "image/png", sizes: "16x16", href: "/icons/favicon-16x16.png" },
            { rel: "icon", type: "image/png", sizes: "32x32", href: "/icons/favicon-32x32.png" },
            { rel: "apple-touch-icon", sizes: "180x180", href: "/icons/apple-touch-icon.png" },
            { rel: "manifest", href: "/icons/site.webmanifest" },
         ],
      },
   },
   runtimeConfig: {
      fireDataBaseUrl:
         "https://huggingface.co/datasets/leveluplevelyn/fire_event_nasaspaceapps/resolve/main/",
   },
   nitro: {
      serverAssets: [
         {
            baseName: "sql",
            dir: fileURLToPath(new URL("./server/sql", import.meta.url)),
         },
      ],
   },
   routeRules: {
      "/": { redirect: "/map" },
   },
});
