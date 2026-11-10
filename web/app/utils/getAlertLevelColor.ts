const colors: Record<number, GridColor> = {
   1: "green",
   2: "yellow",
   3: "orange",
   4: "red",
   5: "darkred",
};

export function getAlertLevelColor(alertLevel: number) {
   return colors[alertLevel] ?? "gray";
}
