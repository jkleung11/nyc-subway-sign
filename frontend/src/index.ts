import axios from 'axios';
import { setTimeout } from 'timers/promises';
import { displayMessage, drawTrainLogo, displayStopName } from './utils';
import { matrix, font } from './matrix';

// Backend API URL (make sure it points to the correct backend URL)
const backendUrl = process.env.SUBWAY_API_URL || 'http://localhost:8000';

interface Arrival {
  route_id: string;
  direction_label: string;
  arrival_mins: number;
}

interface BackendResponse {
  stop_name: string;
  arrivals: Arrival[]
}

// Function to fetch data from the backend and print the status code to the LED matrix
async function fetchArrivals (): Promise<BackendResponse | null> {
  try {
    // Make a POST request to the backend
    const response = await axios.post(`${backendUrl}/times`, {
      gtfs_stop_id: 'A45',
      min_mins: 5,
      max_mins: 25
    });
    console.log(response.status);
    return response.data;
  } catch (error) {
      console.error(`Issue getting times from backend ${error}`);
      return null;
  }
}

let intervalId: NodeJS.Timeout | undefined;
// Main function to start the process
async function fetchAndDisplay() {
  // Fetch data and display the status code on the LED matrix
  
  try {
    const timesData = await fetchArrivals();
    if (timesData && timesData.arrivals.length > 1) {
      for (let i = 0; i < timesData.arrivals.length; i+=2) {
        const train1 = timesData.arrivals[i];
        const train2 = timesData.arrivals[i+1] !== undefined ? timesData.arrivals[i+1] : null;
        matrix.clear();
        // draw first response
        drawTrainLogo(matrix, 1, 2, 4, train1.route_id);
        displayMessage(matrix, 9, 5, train1.direction_label);
        displayMessage(matrix, 46, 5, train1.arrival_mins.toString() + 'min');
        
        if (train2 !== null) {
          drawTrainLogo(matrix, 1, 14, 4, train2.route_id);
          displayMessage(matrix, 9, 17, train2.direction_label);
          displayMessage(matrix, 46, 17, train2.arrival_mins.toString() + 'min');
        }
        
        displayStopName(matrix, font, timesData.stop_name);
  
        matrix.sync();
        await setTimeout(3000);

      }
      console.log(timesData.arrivals);
    } else if (timesData === null) {
      matrix.clear();
      console.log("received null from backend");
      displayMessage(matrix, 0, 0, "empty data");
      matrix.sync();
    } else {
      displayMessage(matrix, 0, 0, "error with api");
      matrix.sync();
    }
  } catch(error) {
      if (intervalId !== undefined) {
        clearInterval(intervalId);
        console.log("cleared interval from timeout")
      }
  }
}

async function main() {
  fetchAndDisplay();
  intervalId = setInterval(fetchAndDisplay, 60000);

}

main();