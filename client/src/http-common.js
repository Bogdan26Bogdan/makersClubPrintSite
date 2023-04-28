import axios from "axios";
// Axios handles the http requests for the app

export default axios.create({
    //base URL is the location that Vue communicates to
    //This will need to be updated to communicat with FLASK - on port 5000?
    baseURL: "http://localhost:8080",
    headers: {
        "Content-Type": "application/json"
    }
});