
import { drawTrainLogo, displayMessage, displayStationName } from './utils';
import { font, matrix } from './matrix';

// Function to loop through the list of messages
async function drawDisplay() {
  
  drawTrainLogo(matrix, 1, 2, 4, 'A');
  displayMessage(matrix, 'Manhattan', 9, 5);
  displayMessage(matrix, '20min', 46, 5);
  
  drawTrainLogo(matrix, 1, 14, 4, '1');
  displayMessage(matrix, 'Uptown', 9, 17);
  displayMessage(matrix, '10min', 46, 17);
  displayStationName(matrix, font, '125th St')
  matrix.sync();
  }


// Main function to start the loop
async function main() {
  console.log('Starting message loop on LED matrix...');
  await drawDisplay(); // Start looping through messages
  setInterval(drawDisplay, 10000)
}

main();
