import axios, { AxiosResponse } from 'axios';
import { LedMatrix, GpioMapping, LedMatrixInstance, Font } from 'rpi-led-matrix';

// Backend API URL (make sure it points to the correct backend URL)
const backendUrl = process.env.SUBWAY_API_URL || 'http://backend:8000';

// LED Matrix setup (adjust according to your specific LED matrix setup)
const matrix = new LedMatrix(
  {
    ...LedMatrix.defaultMatrixOptions(),
    rows: 32,
    cols: 64,
    chainLength: 1,
    hardwareMapping: GpioMapping.AdafruitHat,
  }, {
    ...LedMatrix.defaultRuntimeOptions(),
    gpioSlowdown: 3,
    
  });


// Optional: Load a font for the matrix (this requires a TTF font file to be available on your system)
const fontPath = 'fonts/helvR12.bdf';
const font = new Font('helvR12', fontPath);

// Load the font (if using one)
matrix.font(font);

// Function to fetch data from the backend and print the status code to the LED matrix
async function fetchDataAndDisplay(): Promise<void> {
  try {
    // Make a POST request to the backend
    const response: AxiosResponse = await axios.post(`${backendUrl}/times/`, {
      gtfs_stop_id: 'A24',
      min_mins: 5,
      max_mins: 15
    });

    // Print the HTTP status code on the LED matrix
    const statusCode = response.status;
    console.log(`Received status code: ${statusCode}`);

    // Display the status code on the LED matrix
    displayStatusCode(statusCode);
  } catch (error) {
    // Check if the error is an AxiosError and if it has a response
    if (axios.isAxiosError(error)) {
      if (error.response) {
        // Server responded with a status code other than 2xx
        const statusCode = error.response.status;
        console.error('Error response from backend:', statusCode);
        displayStatusCode(statusCode);
      } else {
        // Network error or no response received
        console.error('Network error or no response from backend:', error.message);
        displayStatusCode('ERR'); // Display "ERR" for network errors
      }
    } else {
      // Some other error occurred
      console.error('Unexpected error:', error);
      displayStatusCode('ERR');
    }
  }
}


// Function to display a status code on the LED matrix
function displayStatusCode(statusCode: number | string): void {
  // Clear the matrix before displaying new content
  matrix.clear();

  // Set color (red for errors, green for success, yellow for other codes)
  if (statusCode === 200 || statusCode === 307) {
    matrix.fgColor(0x00FF00); // Green for success (status code 200)
  } else if (typeof statusCode === 'number' && statusCode >= 400) {
    matrix.fgColor(0xFF0000); // Red for errors (status codes 4xx and 5xx)
  } else {
    matrix.fgColor(0xFFFF00); // Yellow for other codes
  }

  // Display the status code in the center of the LED matrix
  matrix.drawText(`Status: ${statusCode}`, 5, 10);

  // Render the display
  matrix.sync();
}

// Main function to start the process
async function main() {
  // Fetch data and display the status code on the LED matrix
  await fetchDataAndDisplay();

  // Optional: If you want to periodically update the matrix, you can use setInterval
  setInterval(fetchDataAndDisplay, 60000); // e.g., fetch and display every 60 seconds
}

main();




// import axios, { AxiosResponse } from 'axios';
// import { GpioMapping, LedMatrix, LedMatrixInstance, Font, FontInstance } from 'rpi-led-matrix';

// const backendUrl = process.env.SUBWAY_API_URL || 'http://0.0.0.0:8000';

// async function fetchData(): Promise<AxiosResponse> {
//   try {
//     // Make an HTTP GET request to the backend
//     console.log(`requesting to ${backendUrl}`)
//     const response = await axios.post(`${backendUrl}/times`, 
//       { 
//       gtfs_stop_id: 'A24',
//       min_mins: 5,
//       max_mins: 15
//     });
    
//     // Print out the response data (for now, this is simulating the LED matrix output)
//     console.log('Received data from backend:', response.data);
//     return response;

//     // TODO: Replace this with logic to send data to the LED matrix
//   } catch (error) {
//     console.error('Error fetching data from backend:', error);
//     throw error;
//   }
// }

// const matrix = new LedMatrix(
//   {
//     ...LedMatrix.defaultMatrixOptions(),
//     rows: 32,
//     cols: 64,
//     chainLength: 1,
//     hardwareMapping: GpioMapping.AdafruitHat,
//   }, {
//     ...LedMatrix.defaultRuntimeOptions()
//   });

// const font = new Font('helvR12', `${process.cwd()}/fonts/helvR12.bdf`);
// matrix.font(font);


// // Function to continuously loop and fetch data at intervals
// async function startLoop(interval: number, matrix: LedMatrixInstance): Promise<void> {
//   console.log(`Starting loop, fetching data every ${interval}ms...`);

//   // Infinite loop to fetch data continuously
//   while (true) {
//     console.log(`${process.env.SUBWAY_API_URL}`)
//     const mtaData = await fetchData();  // Fetch data from the backend
//     matrix.clear()
//     matrix.drawText(mtaData.data.statusCode, 5, 7)
//     matrix.sync();

//     // Wait for the specified interval before making the next request
//     await new Promise(resolve => setTimeout(resolve, interval));
//   }
// }

// // Start the loop, fetching data every 5 seconds (5000 milliseconds)
// startLoop(5000, matrix).catch(err => console.error('Error in the loop:', err));
