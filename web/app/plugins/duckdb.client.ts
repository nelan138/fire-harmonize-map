import { createBrowserDuckDB } from "~/utils/duckdb-browser";
import { createDuckDBService } from "~/utils/duckdb-service";

export default defineNuxtPlugin(() => {
   const duckdb = createDuckDBService(createBrowserDuckDB);
   const dispose = () => {
      void duckdb.dispose();
   };

   window.addEventListener("pagehide", dispose, { once: true });

   if (import.meta.hot) {
      import.meta.hot.dispose(() => {
         window.removeEventListener("pagehide", dispose);
         dispose();
      });
   }

   return {
      provide: {
         duckdb,
      },
   };
});
