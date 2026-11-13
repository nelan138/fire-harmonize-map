
/*
 * anomaly_engine.ts
 * SFAI anomaly scoring, Chow structural-break test,
 * ENSO climate context, and combined result payload.
 */

// ============================================================
// 1. TYPES
// ============================================================

export type SFAIStatus = "ok" | "no-data" | "no-variance";

export interface SFAIResult {
  zScore: number | null;
  alertLevel: string;
  colorHex: string;
  historicalMean: number | null;
  historicalStd: number | null;
  status: SFAIStatus;
}

export type ChowStatus =
  | "break-detected"
  | "no-significant-break"
  | "inconclusive";

export interface ChowTestResult {
  fStat: number | null;
  pValue: number | null;
  degreesOfFreedom: {
    numerator: number;
    denominator: number;
  };
  status: ChowStatus;

  noSignificantBreakDetected: boolean;

  verdict: string;
}

export interface ClimateContextResult {
  oniIndex: number;
  phase: string;
  explanation: string;
}

export interface FullAnomalyPayload {
  selectedDate: string;
  sfaiMetrics: SFAIResult;
  chowTestVerification: ChowTestResult;
  climateContext: ClimateContextResult | null;
}

// ============================================================
// 2. SFAI CALCULATION
// ============================================================

/**
 * Calculates the Standardized Fire Anomaly Index.
 *
 * Uses population standard deviation, matching the original
 * implementation.
 *
 * historicalVals should contain comparable observations:
 * same location / H3 cell, same calendar month, and
 * harmonized fire data across historical years.
 */
export function calculateSFAI(
  currentVal: number,
  historicalVals: number[]
): SFAIResult {

  if (!Number.isFinite(currentVal) || currentVal < 0) {
    throw new RangeError("Current fire count must be a finite, non-negative number.");
  }

  if (!Array.isArray(historicalVals)) {
    throw new TypeError("Historical values must be an array.");
  }

  if (historicalVals.length === 0) {
    return {
      zScore: null,
      alertLevel: "No Data",
      colorHex: "#9ca3af",
      historicalMean: null,
      historicalStd: null,
      status: "no-data"
    };
  }

  for (const value of historicalVals) {
    if (!Number.isFinite(value) || value < 0) {
      throw new RangeError(
        "Historical fire counts must be finite, non-negative numbers."
      );
    }
  }

  const n = historicalVals.length;

  const mean =
    historicalVals.reduce((sum, value) => sum + value, 0) / n;

  const variance =
    historicalVals.reduce(
      (sum, value) => sum + Math.pow(value - mean, 2),
      0
    ) / n;

  const std = Math.sqrt(variance);

  // A Z-score cannot be calculated when historical
  // standard deviation is zero.
  if (std === 0 || !Number.isFinite(std)) {
    return {
      zScore: null,
      alertLevel: "Unscorable (zero variance)",
      colorHex: "#9ca3af",
      historicalMean: Number(mean.toFixed(2)),
      historicalStd: Number(std.toFixed(2)),
      status: "no-variance"
    };
  }

  const zScore = (currentVal - mean) / std;
  const roundedZ = Number(zScore.toFixed(2));

  // Fire activity classification.
  // ENSO conditions are reported separately.
  if (zScore >= 2.0) {
    return {
      zScore: roundedZ,
      alertLevel: "Extreme Fire Anomaly",
      colorHex: "#7e22ce",
      historicalMean: Number(mean.toFixed(2)),
      historicalStd: Number(std.toFixed(2)),
      status: "ok"
    };
  }

  if (zScore >= 1.5) {
    return {
      zScore: roundedZ,
      alertLevel: "Severe Fire Anomaly",
      colorHex: "#ea580c",
      historicalMean: Number(mean.toFixed(2)),
      historicalStd: Number(std.toFixed(2)),
      status: "ok"
    };
  }

  if (zScore >= 1.0) {
    return {
      zScore: roundedZ,
      alertLevel: "Elevated Fire Activity",
      colorHex: "#f97316",
      historicalMean: Number(mean.toFixed(2)),
      historicalStd: Number(std.toFixed(2)),
      status: "ok"
    };
  }

  if (zScore <= -1.5) {
    return {
      zScore: roundedZ,
      alertLevel: "Unusually Low Fire Activity",
      colorHex: "#1e3a8a",
      historicalMean: Number(mean.toFixed(2)),
      historicalStd: Number(std.toFixed(2)),
      status: "ok"
    };
  }

  return {
    zScore: roundedZ,
    alertLevel: "Normal",
    colorHex: "#22c55e",
    historicalMean: Number(mean.toFixed(2)),
    historicalStd: Number(std.toFixed(2)),
    status: "ok"
  };
}

// ============================================================
// 3. MATHEMATICAL HELPERS FOR THE CHOW TEST
// ============================================================

/**
 * Calculates the natural logarithm of the Gamma function.
 * Uses the Lanczos approximation.
 */
function logGamma(z: number): number {
  const coefficients = [
    676.5203681218851,
    -1259.1392167224028,
    771.3234287776531,
    -176.6150291621406,
    12.507343278686905,
    -0.13857109526572012,
    9.984369578019572e-6,
    1.5056327351493116e-7
  ];

  if (z < 0.5) {
    return Math.log(Math.PI) -
      Math.log(Math.sin(Math.PI * z)) -
      logGamma(1 - z);
  }

  let x = 0.9999999999998099;
  const shifted = z - 1;

  for (let i = 0; i < coefficients.length; i++) {
    x += coefficients[i] / (shifted + i + 1);
  }

  const t = shifted + coefficients.length - 0.5;

  return (
    0.5 * Math.log(2 * Math.PI) +
    (shifted + 0.5) * Math.log(t) -
    t +
    Math.log(x)
  );
}

/**
 * Continued fraction used by the incomplete beta function.
 */
function betaContinuedFraction(
  a: number,
  b: number,
  x: number
): number {
  const maxIterations = 200;
  const epsilon = 3e-14;
  const tiny = 1e-300;

  const qab = a + b;
  const qap = a + 1;
  const qam = a - 1;

  let c = 1;
  let d = 1 - (qab * x) / qap;

  if (Math.abs(d) < tiny) d = tiny;

  d = 1 / d;
  let h = d;

  for (let m = 1; m <= maxIterations; m++) {
    const m2 = 2 * m;

    let aa =
      (m * (b - m) * x) /
      ((qam + m2) * (a + m2));

    d = 1 + aa * d;
    if (Math.abs(d) < tiny) d = tiny;

    c = 1 + aa / c;
    if (Math.abs(c) < tiny) c = tiny;

    d = 1 / d;
    h *= d * c;

    aa =
      (-(a + m) * (qab + m) * x) /
      ((a + m2) * (qap + m2));

    d = 1 + aa * d;
    if (Math.abs(d) < tiny) d = tiny;

    c = 1 + aa / c;
    if (Math.abs(c) < tiny) c = tiny;

    d = 1 / d;

    const delta = d * c;
    h *= delta;

    if (Math.abs(delta - 1) < epsilon) {
      return h;
    }
  }

  throw new Error("Incomplete beta calculation did not converge.");
}

/**
 * Regularized incomplete beta function I_x(a,b).
 */
function regularizedBeta(
  x: number,
  a: number,
  b: number
): number {
  if (x <= 0) return 0;
  if (x >= 1) return 1;

  const logBeta =
    logGamma(a) + logGamma(b) - logGamma(a + b);

  const front = Math.exp(
    a * Math.log(x) +
    b * Math.log1p(-x) -
    logBeta
  );

  if (x < (a + 1) / (a + b + 2)) {
    return (
      front * betaContinuedFraction(a, b, x) / a
    );
  }

  return (
    1 -
    front * betaContinuedFraction(b, a, 1 - x) / b
  );
}

/**
 * Calculates the upper-tail probability of an F distribution.
 *
 * This is the actual p-value used by the Chow test.
 */
function fDistributionSurvival(
  f: number,
  df1: number,
  df2: number
): number {
  if (f < 0 || df1 <= 0 || df2 <= 0) {
    throw new RangeError("Invalid F-distribution arguments.");
  }

  if (f === Infinity) return 0;
  if (f === 0) return 1;

  const x = df2 / (df2 + df1 * f);

  const p = regularizedBeta(
    x,
    df2 / 2,
    df1 / 2
  );

  return Math.max(0, Math.min(1, p));
}

// ============================================================
// 4. LINEAR REGRESSION RSS
// ============================================================

/**
 * Calculates RSS for a linear regression:
 *
 *     y = intercept + slope * x
 *
 * startIndex preserves the original time coordinate
 * when fitting the post-break segment.
 */
function computeRSS(
  data: number[],
  startIndex: number
): number {
  const n = data.length;

  if (n < 3) {
    throw new Error("At least 3 observations are needed per regression.");
  }

  const xMean = startIndex + (n - 1) / 2;
  const yMean = data.reduce((sum, value) => sum + value, 0) / n;

  let numerator = 0;
  let denominator = 0;

  for (let i = 0; i < n; i++) {
    const x = startIndex + i;

    numerator += (x - xMean) * (data[i] - yMean);
    denominator += Math.pow(x - xMean, 2);
  }

  const slope = numerator / denominator;
  const intercept = yMean - slope * xMean;

  let rss = 0;

  for (let i = 0; i < n; i++) {
    const x = startIndex + i;
    const predicted = intercept + slope * x;

    rss += Math.pow(data[i] - predicted, 2);
  }

  return rss;
}

// ============================================================
// 5. CHOW STRUCTURAL BREAK TEST
// ============================================================

/**
 * Chow test for a known breakpoint between two time periods.
 *
 * Null hypothesis:
 * Both periods follow the same linear regression
 * (same intercept and slope).
 *
 * Alternative:
 * At least one regression parameter changes.
 *
 * Significance level: alpha = 0.10
 *
 * IMPORTANT:
 * This test assumes a linear regression model and
 * independent, homoscedastic errors.
 */
export function runChowTest(
  pre2012Counts: number[],
  post2012Counts: number[]
): ChowTestResult {

  const alpha = 0.10;
  const k = 2; // intercept + slope

  const dfNum = k;
  const dfDen =
    pre2012Counts.length + post2012Counts.length - 2 * k;

  const inconclusive = (message: string): ChowTestResult => ({
    fStat: null,
    pValue: null,
    degreesOfFreedom: {
      numerator: dfNum,
      denominator: Math.max(0, dfDen)
    },
    status: "inconclusive",
    noSignificantBreakDetected: false,
    verdict: message
  });

  if (
    !Array.isArray(pre2012Counts) ||
    !Array.isArray(post2012Counts)
  ) {
    throw new TypeError("Both Chow test inputs must be arrays.");
  }

  if (pre2012Counts.length < 3 || post2012Counts.length < 3) {
    return inconclusive(
      "Inconclusive: At least 3 observations are required in each period."
    );
  }

  if (
    ![...pre2012Counts, ...post2012Counts]
      .every(Number.isFinite)
  ) {
    throw new RangeError("Chow test data must contain only finite numbers.");
  }

  if ([...pre2012Counts, ...post2012Counts].some((value) => value < 0)) {
    throw new RangeError("Chow test fire counts must be non-negative.");
  }

  if (dfDen <= 0) {
    return inconclusive(
      "Inconclusive: Not enough residual degrees of freedom."
    );
  }

  const combined = [...pre2012Counts, ...post2012Counts];

  const rssCombined = computeRSS(combined, 0);

  const rssPre = computeRSS(pre2012Counts, 0);

  const rssPost = computeRSS(
    post2012Counts,
    pre2012Counts.length
  );

  const rssSeparate = rssPre + rssPost;

  // RSS should not be negative, but floating-point arithmetic
  // can produce extremely small numerical differences.
  const rssDifference = Math.max(
    0,
    rssCombined - rssSeparate
  );

  const numerator = rssDifference / dfNum;
  const denominator = rssSeparate / dfDen;

  // Detect a zero-residual-variance case.
  const totalMagnitude = combined.reduce(
    (sum, value) => sum + value * value,
    0
  );

  const zeroTolerance =
    Number.EPSILON * Math.max(1, totalMagnitude) * 100;

  let fStat: number;
  let pValue: number;

  if (denominator <= zeroTolerance) {
    if (numerator <= zeroTolerance) {
      return inconclusive(
        "Inconclusive: Both models have essentially zero residual variance. The F-statistic is undefined."
      );
    }

    // Separate regressions fit perfectly, but the pooled
    // regression does not. This is an infinite F-statistic.
    fStat = Infinity;
    pValue = 0;
  } else {
    fStat = numerator / denominator;

    pValue = fDistributionSurvival(
      fStat,
      dfNum,
      dfDen
    );
  }

  const hasSignificantBreak = pValue <= alpha;

  if (hasSignificantBreak) {
    return {
      fStat: Number.isFinite(fStat)
        ? Number(fStat.toFixed(6))
        : null,
      pValue: Number(pValue.toPrecision(6)),
      degreesOfFreedom: {
        numerator: dfNum,
        denominator: dfDen
      },
      status: "break-detected",
      noSignificantBreakDetected: false,
      verdict:
        "Evidence of a statistically significant structural break at the supplied breakpoint (p <= 0.10)."
    };
  }

  return {
    fStat: Number(fStat.toFixed(6)),
    pValue: Number(pValue.toPrecision(6)),
    degreesOfFreedom: {
      numerator: dfNum,
      denominator: dfDen
    },
    status: "no-significant-break",
    noSignificantBreakDetected: true,
    verdict:
      "No statistically significant structural break detected (p > 0.10); this does not prove the absence of a break."
  };
}

// ============================================================
// 6. ENSO / ONI CLIMATE CONTEXT
// ============================================================

/**
 * Provides climate context from an ONI value.
 *
 * A single ONI value is not enough to establish an
 * official El NiÃ±o or La NiÃ±a episode. Official event
 * classification also considers persistence over time.
 */
export function getClimateContext(
  oniIndex: number,
  dateStr: string
): ClimateContextResult {

  if (!Number.isFinite(oniIndex)) {
    throw new RangeError("ONI must be a finite number.");
  }

  if (oniIndex >= 0.5) {
    return {
      oniIndex,
      phase: "Warm ENSO conditions",
      explanation:
        `${dateStr}: ONI is +${oniIndex}. ` +
        "This indicates warm ENSO conditions. " +
        "They may provide climate context for observed fire activity, " +
        "but this value alone does not prove that ENSO caused a fire spike."
    };
  }

  if (oniIndex <= -0.5) {
    return {
      oniIndex,
      phase: "Cool ENSO conditions",
      explanation:
        `${dateStr}: ONI is ${oniIndex}. ` +
        "This indicates cool ENSO conditions. " +
        "Their local relationship with fire activity depends on regional climate."
    };
  }

  return {
    oniIndex,
    phase: "Neutral ENSO conditions",
    explanation:
      `${dateStr}: ONI is ${oniIndex}. ` +
      "This value is within the neutral threshold range."
  };
}

// ============================================================
// 7. COMBINED ANOMALY PAYLOAD
// ============================================================

export function generateAnomalyPayload(
  currentVal: number,
  historicalVals: number[],
  pre2012Counts: number[],
  post2012Counts: number[],
  oniIndex: number | null,
  dateStr: string
): FullAnomalyPayload {

  return {
    selectedDate: dateStr,

    sfaiMetrics: calculateSFAI(
      currentVal,
      historicalVals
    ),

    chowTestVerification: runChowTest(
      pre2012Counts,
      post2012Counts
    ),

    climateContext: oniIndex === null
      ? null
      : getClimateContext(oniIndex, dateStr)
  };
}
