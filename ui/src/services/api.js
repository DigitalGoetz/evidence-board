import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const fetchEvidenceById = async (evidenceId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/evidence/${evidenceId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching evidence:', error);
    throw error;
  }
};
