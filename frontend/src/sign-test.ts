import {
  LedMatrix,
  GpioMapping,
  Font
} from 'rpi-led-matrix';

import { getTrainColor } from './colors';




// LED Matrix setup (adjust according to your specific LED matrix setup)
const matrix = new LedMatrix({
  ...LedMatrix.defaultMatrixOptions(),
  rows: 32,               
  cols: 64,               
  brightness: 50,
  chainLength: 1,
  hardwareMapping: GpioMapping.AdafruitHat,
  showRefreshRate: true,
}, {
  ...LedMatrix.defaultRuntimeOptions(),
  gpioSlowdown: 3

});

// Optional: Load a font for the matrix (this requires a BDF font file to be available)
const fontPath = 'fonts/tom-thumb.bdf';  // Replace with your font path
const font = new Font('tom-thumb', fontPath);

// Load the font (if using one)
matrix.font(font);

// List of strings to display on the LED matrix
const messages: string[] = [
  "Kingston 13min",
  "Uptown",
  "Goodbye!"
];

// Function to display a message on the LED matrix
function displayMessage(message: string, x: number, y: number): void {
  // Clear the matrix before displaying new content

  // Set text color (you can change the color as needed)

  matrix.fgColor(0x00FF00); // Green color
  // // Display the message in the center of the LED matrix
  matrix.drawText(message, x, y);  // Adjust the x, y coordinates as needed

  // // Render the display
  matrix.sync();
}

function drawTrainCircle(startX: number, startY: number, width: number, train: string): void {
  const color = getTrainColor(train)
  matrix.fgColor(color);
  matrix.drawLine(startX+2, startY+0, startX+width, startY+0);
  matrix.drawLine(startX+1, startY+1, startX+width+1, startY+1);
  matrix.drawLine(startX+0, startY+2, startX+width+2, startY+2);
  matrix.drawLine(startX+0, startY+3, startX+width+2, startY+3);
  matrix.drawLine(startX+0, startY+4, startX+width+2, startY+4);
  matrix.drawLine(startX+0, startY+5, startX+width+2, startY+5);
  matrix.drawLine(startX+0, startY+6, startX+width+2, startY+6);
  matrix.drawLine(startX+1, startY+7, startX+width+1, startY+7);
  matrix.drawLine(startX+2, startY+8, startX+width+0,  startY+8);
  matrix.fgColor(0x000000);
  matrix.drawText(train, startX+2, startY+3);
}

// Function to loop through the list of messages
async function loopMessages() {
  while (true) {
    drawTrainCircle(1, 2, 4, 'A');
    displayMessage('Manhattan', 9, 5);
    displayMessage('20min', 46, 5);

    drawTrainCircle(1, 14, 4, '1');
    displayMessage('Uptown', 9, 17);
    displayMessage('10min', 46, 17);


    const stationName = 'Franklin Av';
    const nameWidth = font.stringWidth(stationName);
    const centeredX = Math.floor((matrix.width() - nameWidth) / 2);
    displayMessage(stationName, centeredX, 26);
    

  //   for (const message of messages) {
  //     // Display each message
  //     // displayMessage(message);

  //     // Wait for 2 seconds before showing the next message
  //     await delay(2000);
  //   }
  }
}

// Helper function to add a delay (simulates sleep)
function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Main function to start the loop
async function main() {
  console.log('Starting message loop on LED matrix...');
  await loopMessages(); // Start looping through messages
}

main();
