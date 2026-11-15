export type HeatmapGridColor = "gray" | "neutral" | "purple" | "red" | "orange" | "gold" | "yellow";

const colorClasses: Record<HeatmapGridColor, string> = {
   gray: "bg-muted",
   neutral: "bg-primary/20",
   purple: "bg-[#420a68] text-white",
   red: "bg-[#932667] text-white",
   orange: "bg-[#dd513a] text-black",
   gold: "bg-[#fca50a] text-black",
   yellow: "bg-[#fcffa4] text-black",
};

export function getHeatmapGridColor(color: HeatmapGridColor) {
   return colorClasses[color];
}
