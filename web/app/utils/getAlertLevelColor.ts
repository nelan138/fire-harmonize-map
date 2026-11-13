const colors: Record<number, HeatmapGridColor> = {
   1: "purple",
   2: "red",
   3: "orange",
   4: "gold",
   5: "yellow",
};

export function getAlertLevelColor(alertLevel: number) {
   return colors[alertLevel] ?? "gray";
}