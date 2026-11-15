import { describe, expect, it } from "vitest";

import {
   calculateSFAI,
   generateAnomalyPayload,
   getClimateContext,
   runChowTest,
} from "../app/utils/anomaly_engine";

describe("calculateSFAI", () => {
   it("scores a current month against comparable historical months", () => {
      const result = calculateSFAI(30, [10, 20, 30]);

      console.log("calculateSFAI(30, [10, 20, 30]) =", result);

      expect(result.zScore).toBe(1.22);
      expect(result.alertLevel).toBe("Elevated Fire Activity");
      expect(result.historicalMean).toBe(20);
      expect(result.status).toBe("ok");
   });

   it("reports missing history and zero variance explicitly", () => {
      expect(calculateSFAI(12, []).status).toBe("no-data");
      expect(calculateSFAI(12, [5, 5, 5]).status).toBe("no-variance");
   });

   it("classifies using the unrounded z-score at alert thresholds", () => {
      expect(calculateSFAI(2.996, [0, 2]).alertLevel).toBe("Severe Fire Anomaly");
   });

   it("rejects invalid fire counts", () => {
      expect(() => calculateSFAI(-1, [1, 2])).toThrow(RangeError);
      expect(() => calculateSFAI(1, [Number.NaN])).toThrow(RangeError);
   });
});

describe("runChowTest", () => {
   it("detects a large level change at the supplied break", () => {
      const result = runChowTest(
         [10, 11, 9, 10, 11, 9],
         [30, 31, 29, 30, 31, 29],
      );

      console.log(
         "runChowTest([10, 11, 9, 10, 11, 9], [30, 31, 29, 30, 31, 29]) =",
         result,
      );

      expect(result.status).toBe("break-detected");
      expect(result.pValue).not.toBeNull();
      expect(result.pValue!).toBeLessThanOrEqual(0.1);
      expect(result.noSignificantBreakDetected).toBe(false);
      expect(result.verdict).toContain("Evidence of a statistically significant structural break");
   });

   it("returns inconclusive when either period is too short", () => {
      expect(runChowTest([1, 2], [3, 4, 5]).status).toBe("inconclusive");
   });

   it("rejects negative fire counts", () => {
      expect(() => runChowTest([-1, 2, 3], [4, 5, 6])).toThrow(RangeError);
   });
});

describe("getClimateContext", () => {
   it("labels ONI context without claiming causation", () => {
      const result = getClimateContext(0.8, "2024-01");

      console.log('getClimateContext(0.8, "2024-01") =', result);

      expect(result.phase).toBe("Warm ENSO conditions");
      expect(result.explanation).toContain("does not prove that ENSO caused");
   });
});

describe("generateAnomalyPayload", () => {
   it("prints the combined anomaly result", () => {
      const result = generateAnomalyPayload(
         30,
         [10, 20, 30],
         [10, 11, 9, 10, 11, 9],
         [30, 31, 29, 30, 31, 29],
         0.8,
         "2024-01",
      );

      console.log("generateAnomalyPayload(...) =", result);

      expect(result.selectedDate).toBe("2024-01");
      expect(result.sfaiMetrics.zScore).toBe(1.22);
      expect(result.chowTestVerification.status).toBe("break-detected");
      expect(result.climateContext.phase).toBe("Warm ENSO conditions");
   });

   it("leaves climate context unavailable when no ONI value is supplied", () => {
      const result = generateAnomalyPayload(
         30,
         [10, 20, 30],
         [10, 11, 9, 10, 11, 9],
         [30, 31, 29, 30, 31, 29],
         null,
         "2024-01",
      );

      expect(result.climateContext).toBeNull();
   });
});
