import { existsSync } from "node:fs";
import { mkdir, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { DuckDBInstance } from "@duckdb/node-api";

import { generateAnomalyPayload } from "../app/utils/anomaly_engine.ts";

const scriptDirectory = fileURLToPath(new URL(".", import.meta.url));
const defaultParquetPath = resolve(
   scriptDirectory,
   "../../../calibrated-data/processed/calibrated/harmonized_fire_monthly.parquet",
);
const defaultOutputPath = resolve(
   scriptDirectory,
   "../public/data/anomaly_diagnostics.csv",
);

function option(name, fallback) {
   const index = process.argv.indexOf(`--${name}`);
   if (index === -1) return fallback;

   const value = process.argv[index + 1];
   if (!value || value.startsWith("--")) {
      throw new Error(`Missing value for --${name}.`);
   }
   return value;
}

function sqlString(value) {
   return `'${String(value).replaceAll("'", "''")}'`;
}

function finiteNumber(value, field, { nullable = false } = {}) {
   if (nullable && (value === null || value === undefined)) return null;
   const number = Number(value);
   if (!Number.isFinite(number)) {
      throw new TypeError(`Parquet field ${field} must be a finite number.`);
   }
   return number;
}

function csvCell(value) {
   if (value === null || value === undefined) return "";
   const text = Array.isArray(value) ? value.join(";") : String(value);
   return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function toCsv(records) {
   const columns = Object.keys(records[0] ?? {});
   return [
      columns.map(csvCell).join(","),
      ...records.map((record) => columns.map((column) => csvCell(record[column])).join(",")),
   ].join("\r\n") + "\r\n";
}

function normalizeRow(row) {
   const year = finiteNumber(row.year, "year");
   const month = finiteNumber(row.month, "month");
   const biomeId = finiteNumber(row.biome_id, "biome_id");
   const adjustedFireCount = finiteNumber(row.adj_fire_count, "adj_fire_count");
   if (!Number.isInteger(year) || !Number.isInteger(month) || month < 1 || month > 12) {
      throw new TypeError("Parquet year and month fields must be valid integers.");
   }
   if (!Number.isInteger(biomeId) || adjustedFireCount < 0) {
      throw new TypeError("Parquet biome_id must be an integer and fire counts non-negative.");
   }

   return {
      region_id: String(row.region_id),
      h3_index: String(row.h3_index ?? "N/A"),
      year,
      month,
      biome_id: biomeId,
      lat_centroid: finiteNumber(row.lat_centroid, "lat_centroid", { nullable: true }),
      lon_centroid: finiteNumber(row.lon_centroid, "lon_centroid", { nullable: true }),
      raw_modis_count: finiteNumber(row.raw_modis_count, "raw_modis_count"),
      raw_viirs_count: finiteNumber(row.raw_viirs_count, "raw_viirs_count"),
      adj_fire_count: adjustedFireCount,
      adj_frp_mw: finiteNumber(row.adj_frp_mw, "adj_frp_mw", { nullable: true }),
   };
}

function groupKey(row) {
   return [row.region_id, row.h3_index, row.biome_id, row.month].join("|");
}

function createDiagnosticRecords(rows) {
   if (rows.length === 0) {
      throw new Error("The calibrated Parquet query returned no monthly records.");
   }

   const groups = new Map();
   const regionYearRanges = new Map();
   for (const row of rows) {
      const range = regionYearRanges.get(row.region_id) ?? { min: row.year, max: row.year };
      range.min = Math.min(range.min, row.year);
      range.max = Math.max(range.max, row.year);
      regionYearRanges.set(row.region_id, range);

      const key = groupKey(row);
      if (!groups.has(key)) groups.set(key, new Map());
      const years = groups.get(key);
      if (years.has(row.year)) {
         throw new Error(`Duplicate monthly group in Parquet for ${key}, year ${row.year}.`);
      }
      years.set(row.year, row);
   }

   const records = [];
   for (const years of groups.values()) {
      const template = years.values().next().value;
      const yearRange = regionYearRanges.get(template.region_id);
      const annual = [];
      for (let year = yearRange.min; year <= yearRange.max; year++) {
         annual.push(years.get(year) ?? {
            ...template,
            year,
            lat_centroid: null,
            lon_centroid: null,
            raw_modis_count: 0,
            raw_viirs_count: 0,
            adj_fire_count: 0,
            adj_frp_mw: 0,
         });
      }

      const pre2012 = annual.filter((row) => row.year < 2012);
      const post2012 = annual.filter((row) => row.year >= 2012);
      for (let index = 0; index < annual.length; index++) {
         const current = annual[index];
         const history = annual.slice(0, index);
         const payload = generateAnomalyPayload(
            current.adj_fire_count,
            history.map((row) => row.adj_fire_count),
            pre2012.map((row) => row.adj_fire_count),
            post2012.map((row) => row.adj_fire_count),
            null,
            `${current.year}-${String(current.month).padStart(2, "0")}`,
         );
         const sfai = payload.sfaiMetrics;
         const chow = payload.chowTestVerification;

         records.push({
            region_id: current.region_id,
            h3_index: current.h3_index,
            year: current.year,
            month: current.month,
            biome_id: current.biome_id,
            lat_centroid: current.lat_centroid,
            lon_centroid: current.lon_centroid,
            raw_modis_count: current.raw_modis_count,
            raw_viirs_count: current.raw_viirs_count,
            adj_fire_count: current.adj_fire_count,
            adj_frp_mw: current.adj_frp_mw,
            selected_date: payload.selectedDate,
            sfai_baseline_start_year: history[0]?.year ?? null,
            sfai_baseline_end_year: history.at(-1)?.year ?? null,
            sfai_baseline_year_count: history.length,
            sfai_baseline_years: history.map((row) => row.year),
            sfai_historical_mean: sfai.historicalMean,
            sfai_historical_std: sfai.historicalStd,
            sfai_z_score: sfai.zScore,
            sfai_alert_level: sfai.alertLevel,
            sfai_alert_color_hex: sfai.colorHex,
            sfai_status: sfai.status,
            chow_break_year: 2012,
            chow_pre_year_count: pre2012.length,
            chow_post_year_count: post2012.length,
            chow_f_stat: chow.fStat,
            chow_p_value: chow.pValue,
            chow_df_numerator: chow.degreesOfFreedom.numerator,
            chow_df_denominator: chow.degreesOfFreedom.denominator,
            chow_status: chow.status,
            chow_no_significant_break_detected: chow.noSignificantBreakDetected,
            chow_verdict: chow.verdict,
            oni_index: null,
            enso_phase: null,
            enso_explanation: null,
            spatial_resolution: current.h3_index === "N/A"
               ? "regional aggregate; centroid varies by year"
               : "H3 cell",
         });
      }
   }

   return records.sort((a, b) =>
      a.region_id.localeCompare(b.region_id) ||
      a.biome_id - b.biome_id ||
      a.month - b.month ||
      a.year - b.year,
   );
}

async function main() {
   const inputPath = resolve(option("parquet", defaultParquetPath));
   const outputPath = resolve(option("out", defaultOutputPath));
   const region = option("region", "INDOCHINA");
   if (!existsSync(inputPath)) {
      throw new Error(`Monthly calibrated Parquet file was not found: ${inputPath}`);
   }

   const instance = await DuckDBInstance.create(":memory:");
   const connection = await instance.connect();
   try {
      const regionClause = region.toLowerCase() === "all"
         ? ""
         : `WHERE region_id = ${sqlString(region)}`;
      const result = await connection.runAndReadAll(`
         SELECT
            region_id,
            year,
            month,
            h3_index,
            biome_id,
            AVG(lat_centroid) AS lat_centroid,
            AVG(lon_centroid) AS lon_centroid,
            SUM(raw_modis_count) AS raw_modis_count,
            SUM(raw_viirs_count) AS raw_viirs_count,
            SUM(adj_fire_count) AS adj_fire_count,
            SUM(adj_frp_mw) AS adj_frp_mw
         FROM read_parquet(${sqlString(inputPath)})
         ${regionClause}
         GROUP BY region_id, year, month, h3_index, biome_id
         ORDER BY region_id, biome_id, month, year
      `);
      const inputRows = result.getRowObjectsJson().map(normalizeRow);
      const records = createDiagnosticRecords(inputRows);

      await mkdir(dirname(outputPath), { recursive: true });
      await writeFile(outputPath, toCsv(records), "utf8");
      console.log(`Read ${inputRows.length} calibrated monthly rows.`);
      console.log(`Wrote ${records.length} anomaly diagnostic rows to ${outputPath}`);
      console.log(`Fields: ${Object.keys(records[0]).join(", ")}`);
   } finally {
      connection.closeSync();
   }
}

main().catch((error) => {
   console.error(error instanceof Error ? error.message : error);
   process.exitCode = 1;
});
