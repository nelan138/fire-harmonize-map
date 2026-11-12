import { handleMonthlyQuery } from "../utils/monthly-handler";

export default defineEventHandler((event) => handleMonthlyQuery(event, "fire-density.sql"));
