import {
  LedMatrix,
  GpioMapping,
  Font
} from 'rpi-led-matrix';

// const matrix = new LedMatrix(
//   {
//     ...LedMatrix.defaultMatrixOptions(),
//     rows: 32,
//     cols: 64,
//     chainLength: 1,
//     hardwareMapping: GpioMapping.AdafruitHat
//   },
//   {
//     ...LedMatrix.defaultRuntimeOptions(),
//     gpioSlowdown: 1,
//   }
// );

// matrix 
//   .brightness(100) // set the panel brightness to 100%
//   .fgColor(0x63bc41) // set the active color to blue
//   .fill()
//   .sync();

//   import { LedMatrix, GpioMapping, Font } from 'rpi-led-matrix';

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

  function drawCircle(x_start: number, y_start: number, width: number, color: number): void {
    matrix.fgColor(color);
    matrix.drawLine(x_start+2, y_start+0, x_start+width, y_start+0);
    matrix.drawLine(x_start+1, y_start+1, x_start+width+1, y_start+1);
    matrix.drawLine(x_start+0, y_start+2, x_start+width+2, y_start+2);
    matrix.drawLine(x_start+0, y_start+3, x_start+width+2, y_start+3);
    matrix.drawLine(x_start+0, y_start+4, x_start+width+2, y_start+4);
    matrix.drawLine(x_start+0, y_start+5, x_start+width+2, y_start+5);
    matrix.drawLine(x_start+0, y_start+6, x_start+width+2, y_start+6);
    matrix.drawLine(x_start+1, y_start+7, x_start+width+1, y_start+7);
    matrix.drawLine(x_start+2, y_start+8, x_start+width, y_start+8);
    matrix.fgColor(0x000000);
  }
  
  // Function to loop through the list of messages
  async function loopMessages() {
    while (true) {
      drawCircle(1, 2, 4, 0x0039A6);
      matrix.drawText('C', 3, 5);
      displayMessage('Manhattan', 9, 5);
      displayMessage('20min', 46, 5);

      drawCircle(1, 16, 4, 0x0039A6);
      matrix.drawText('A', 3, 19)
      displayMessage('Uptown', 9, 19);
      displayMessage('10min', 46, 19);
      

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
  