import { fetchArrivals } from './api/api';
import { setTimeout } from 'timers/promises';
import { displayArrivals, displayError, DisplayErrorType } from './display/utils';
import { matrix } from './display/matrix';

// Backend API URL (make sure it points to the correct backend URL)
const backendUrl = process.env.SUBWAY_API_URL || 'http://localhost:8000';
const gtfsStopIds = process.env.GTFS_STOP_IDS || 'A45,S01';
const minMins = Number(process.env.MIN_MINS) || 3;
const maxMins = Number(process.env.MAX_MINS) || 15;


const stopIds =
  gtfsStopIds
    .split(',')
    .map((s) => s.trim())
    .filter((s) => s.length > 0);

async function fetchAndDisplayStop(stopId: string) {
  const timesData = await fetchArrivals(backendUrl, stopId, minMins, maxMins);
  // early exit
  if ("error" in timesData) {
    displayError(matrix, DisplayErrorType.ApiError);
    return;
  }

  const { stopName, arrivals } = timesData;

  if (arrivals.length === 0) {
    displayError(matrix, DisplayErrorType.NoTrains, stopName);
    return;
  }

  for (let i = 0; i < timesData.arrivals.length; i += 2) {
    const first = timesData.arrivals[i];
    const second = timesData.arrivals[i + 1];

    displayArrivals(matrix, stopName, first, second);

    await setTimeout(5000);

  }
  console.log(timesData.arrivals);

}


async function mainLoop() {
  while (true) {
    try {
      for (const stopId of stopIds) {
        await fetchAndDisplayStop(stopId)
        await setTimeout(2000);
      }
    } catch (err) {
      console.error('Unexpected error in mainLoop:', err);
      displayError(matrix, DisplayErrorType.ApiError);

      await setTimeout(5000);
    }
  }
}

mainLoop();