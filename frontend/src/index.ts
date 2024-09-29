import axios, { AxiosResponse } from 'axios';
import { displayMessage, drawTrainLogo } from './utils';
import { matrix } from './matrix';

// Backend API URL (make sure it points to the correct backend URL)
const backendUrl = process.env.SUBWAY_API_URL || 'http://localhost:8000';

interface Arrival {
  route_id: string
}
interface BackendResponse {
  arrivals: Arrival[]
}

// Function to fetch data from the backend and print the status code to the LED matrix
async function fetchArrivals (): Promise<BackendResponse> {
  try {
    // Make a POST request to the backend
    const response = await axios.post(`${backendUrl}/times`, {
      gtfs_stop_id: 'A24',
      min_mins: 5,
      max_mins: 15
    });
    return response.data;
  } catch (error) {
      console.error(`Issue getting times from backend`);
      throw new Error(`${error}`);
  }
}





// Main function to start the process
async function main() {
  // Fetch data and display the status code on the LED matrix
  const timesData = await fetchArrivals();
  if (timesData.arrivals.length > 1) {
    const train1 = timesData.arrivals[0].route_id;
    const train2 = timesData.arrivals[1].route_id;
    matrix.clear();
    drawTrainLogo(matrix, 1, 2, 4, train1);
    drawTrainLogo(matrix, 1, 14, 4, train2);
    matrix.sync();
  }
  console.log(timesData.arrivals);


  setInterval(fetchArrivals, 10000); //
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
