import { LedMatrixInstance, FontInstance } from "rpi-led-matrix";

import { Arrival } from "../api/api";
import { getTrainColor } from "./colors";
import { font } from "./matrix";


// define an interface for our display slots
interface ArrivalSlot {
  logoX: number;
  logoY: number;
  logoWidth: number;
  stopLabelX: number;
  timeX: number;
  messageY: number;
}

const slots: ArrivalSlot[] = [
  { logoX: 1, logoY: 2, logoWidth: 4, stopLabelX: 9, timeX: 46, messageY: 5 },
  { logoX: 1, logoY: 14, logoWidth: 4, stopLabelX: 9, timeX: 46, messageY: 17 }
]

export enum DisplayErrorType {
  NoTrains = "no trains",
  ApiError = "api error"
}


export function drawTrainLogo(matrix: LedMatrixInstance, x: number, y: number,
  width: number, train: string): void {
  const color = getTrainColor(train);
  matrix.fgColor(color);
  matrix.drawLine(x + 2, y + 0, x + width + 0, y + 0);
  matrix.drawLine(x + 1, y + 1, x + width + 1, y + 1);
  matrix.drawLine(x + 0, y + 2, x + width + 2, y + 2);
  matrix.drawLine(x + 0, y + 3, x + width + 2, y + 3);
  matrix.drawLine(x + 0, y + 4, x + width + 2, y + 4);
  matrix.drawLine(x + 0, y + 5, x + width + 2, y + 5);
  matrix.drawLine(x + 0, y + 6, x + width + 2, y + 6);
  matrix.drawLine(x + 1, y + 7, x + width + 1, y + 7);
  matrix.drawLine(x + 2, y + 8, x + width + 0, y + 8);
  matrix.fgColor(0x00000);
  matrix.drawText(train, x + 2, y + 3);
}

/**
 * If stopLabel is too long, use Uptown or Downtown
 * Otherwise return stopLabel
 * @param stopLabel direction label of the train
 * @param directionLetter N or S
 * @returns string
 */
export function processStopLabel(stopLabel: string, directionLetter: string): string {
  // sometimes a stop label is too long for our display
  // if we're too long, default to Uptown / Downtown 
  if (directionLetter !== "N" && directionLetter !== "S") {
    throw new Error("Invalid direction letter");
  }

  if (stopLabel.length > 11) {
    return directionLetter === "N" ? "Uptown" : "Downtown";
  }

  return stopLabel;
}

// Function to display a message on the LED matrix
function displayMessage(
  matrix: LedMatrixInstance,
  x: number, 
  y: number, 
  message: string, 
  color: number = 0x00FF00) {
    matrix.fgColor(color);
    matrix.drawText(message, x, y);
}

function displayStopName(matrix: LedMatrixInstance, font: FontInstance, stopName: string, y: number = 26) {
  const nameWidth = font.stringWidth(stopName);
  const centered = Math.floor((matrix.width() - nameWidth) / 2);
  displayMessage(matrix, centered, y, stopName);
}

/**
 * Wrapper util for displaying an arrival in a slot on matrix
 * 
 * @param matrix the matrix instance for writing.
 * @param arrival arrival interface with information on arrival.
 * @param slot either first or second arrival slot for coordinates on writing
 * @returns void
 */
function displayArrival(matrix: LedMatrixInstance, arrival: Arrival, slot: ArrivalSlot) {
  drawTrainLogo(matrix, slot.logoX, slot.logoY, slot.logoWidth, arrival.route_id);

  const stopLabel = processStopLabel(arrival.direction_label, arrival.direction_letter);
  displayMessage(matrix, slot.stopLabelX, slot.messageY, stopLabel);

  const arrivalTimeMessage = arrival.arrival_mins.toString() + 'min';
  displayMessage(matrix, slot.timeX, slot.messageY, arrivalTimeMessage);

}

/**
 * Display two arrivals on matrix, second arrival is optional
 * @param matrix the matrix instance for writing
 * @param first first arrival to display
 * @param second second arrival (if not empty) to display
 * @retruns void
 */

export function displayArrivals(
  matrix: LedMatrixInstance,
  stopName: string,
  first: Arrival,
  second?: Arrival) {

  matrix.clear();

  const firstSlot = slots[0];
  displayArrival(matrix, first, firstSlot);

  if (second != null) {
    const secondSlot = slots[1];
    displayArrival(matrix, second, secondSlot);
  }
  displayStopName(matrix, font, stopName)

  matrix.sync();
}

export function displayError(
  matrix: LedMatrixInstance,
  errorType: DisplayErrorType,
  stopName?: string,
  x: number = 1,
  y: number = 2) {

  matrix.clear();
  displayMessage(matrix, x, y, errorType)
  if (errorType === DisplayErrorType.NoTrains && stopName) {
    displayStopName(matrix, font, stopName);
  }
  matrix.sync();

} 