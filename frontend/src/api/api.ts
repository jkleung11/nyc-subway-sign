import axios from "axios";

// interfaces for responses
interface Arrival {
    route_id: string;
    direction_label: string;
    direction_letter: string;
    arrival_mins: number;
}

interface BackendResponse {
    stop_name: string;
    arrivals: Arrival[];
}

interface ApiErrorResponse {
    error: string;
}

export async function fetchArrivals(backendUrl: string, stopId: string, minMins: number, maxMins: number): Promise<BackendResponse | ApiErrorResponse> {
    try {
        const response = await axios.post<BackendResponse>(`${backendUrl}/times`, {
            gtfs_stop_id: stopId,
            min_mins: minMins,
            max_mins: maxMins
        });
        console.log(response.status);
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            console.error("Axios error details:", error.response?.data);
            const errorMessage = error.response?.data?.message || "Unable to get arrival times due to an Axios error.";
            return { error: errorMessage };
        } else {
            console.error("Error fetching arrivals:", error);
            // Use String(error) to ensure the error is represented as a string.
            return { error: `Unable to get arrival times due to error: ${String(error)}` };
        }
    }
}