import { LedMatrixInstance, FontInstance } from "rpi-led-matrix";
import { getTrainColor } from "./colors";

// Function to display a message on the LED matrix
export function displayMessage(matrix: LedMatrixInstance, 
  x: number, y: number, message: string, color: number=0x00FF00): void {
  matrix.fgColor(color);
  matrix.drawText(message, x, y);
}

export function displayStopName(matrix: LedMatrixInstance, font: FontInstance, 
  stopName: string, y: number=26): void {
  const nameWidth = font.stringWidth(stopName);
  const centered = Math.floor((matrix.width() - nameWidth)/2);
  displayMessage(matrix, centered, y, stopName);
}

export function drawTrainLogo(matrix: LedMatrixInstance, x: number, y: number,
  width: number, train: string): void {
    const color = getTrainColor(train);
    matrix.fgColor(color)
    matrix.fgColor(color);
    matrix.drawLine(x+2, y+0, x+width+0, y+0);
    matrix.drawLine(x+1, y+1, x+width+1, y+1);
    matrix.drawLine(x+0, y+2, x+width+2, y+2);
    matrix.drawLine(x+0, y+3, x+width+2, y+3);
    matrix.drawLine(x+0, y+4, x+width+2, y+4);
    matrix.drawLine(x+0, y+5, x+width+2, y+5);
    matrix.drawLine(x+0, y+6, x+width+2, y+6);
    matrix.drawLine(x+1, y+7, x+width+1, y+7);
    matrix.drawLine(x+2, y+8, x+width+0, y+8);
    matrix.fgColor(0x00000);
    matrix.drawText(train, x+2, y+3);
}