import axios from "axios";

const API_BASE_URL = "http://localhost:8000"; // Ensure this matches your backend URL

export const factCheckText = async (text: string) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/fact-check-text`, { text });
    return response.data;
  } catch (error) {
    console.error("Error fetching text analysis:", error);
    return null;
  }
};

export const factCheckLink = async (url: string) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/fact-check-link`, { url });
    return response.data;
  } catch (error) {
    console.error("Error fetching link analysis:", error);
    return null;
  }
};
