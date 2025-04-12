enum Colors {
  Blue = 0x0039A6,
  Orange = 0xFF6319,
  LightGreen = 0x6CBE45,
  Brown = 0x996633,
  Gray = 0xA7A9AC,
  Yellow = 0xFCCC0A,
  Red = 0xEE352E,
  DarkGreen = 0x00933C,
  Purple = 0xB933AD,
}

const TrainColors: Record<Colors, string[]> = {
  [Colors.Blue]: ["A", "C", "E"],
  [Colors.Orange]: ["B", "D", "F", "M"],
  [Colors.LightGreen]: ["G"],
  [Colors.Brown]: ["J", "Z"],
  [Colors.Gray]: ["L", "S"],
  [Colors.Yellow]: ["N", "Q", "R", "W"],
  [Colors.Red]: ["1", "2", "3"],
  [Colors.DarkGreen]: ["4", "5", "6"],
  [Colors.Purple]: ["7"]
}

export function getTrainColor(trainName: string): Colors | number{
  // Loop through the TrainColors object
  for (const [color, trains] of Object.entries(TrainColors)) {
    if (trains.includes(trainName)) {
      return parseInt(color) as Colors;  // Convert string key back to enum type
    }
  }
  // Default to white if the train name is not found
  return 0xFFFFFF;
}