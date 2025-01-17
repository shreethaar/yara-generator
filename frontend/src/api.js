import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000'; // Flask back-end URL

export const generateYaraRule = async (ruleData) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/generate`, ruleData);
        return response.data;
    } catch (error) {
        console.error('Error generating YARA rule:', error);
        throw error;
    }
};
