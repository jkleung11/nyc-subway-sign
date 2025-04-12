
import { drawTrainLogo, displayMessage, displayStopName } from './display/utils';
import { font, matrix } from './display/matrix';

// Function to loop through the list of messages
async function drawDisplay() {
  
  drawTrainLogo(matrix, 1, 2, 4, 'A');
  displayMessage(matrix, 9, 5, 'Manhattan');
  displayMessage(matrix, 46, 5, '20 min');
  
  drawTrainLogo(matrix, 1, 14, 4, '1');
  displayMessage(matrix, 9, 17, 'Uptown');
  displayMessage(matrix, 46, 17, '10 min');
  displayStopName(matrix, font, '125th St')
  matrix.sync();
  }


// Main function to start the loop
async function main() {
  console.log('Starting message loop on LED matrix...');
  await drawDisplay(); // Start looping through messages
  setInterval(drawDisplay, 10000)
}

main();
