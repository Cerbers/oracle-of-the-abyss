import { useState } from 'react';
import axios from 'axios';

const UserInputBox = ({ onAnalysisReceived }) => {
    const [writing, setWriting] = useState('');
    const [title, setTitle] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    
    const handleSubmit = async (e) => {
        e.preventDefault();
    
        if (!writing.trim()) return;

        setIsLoading(true);
    
        try {
        // Use environment variable
            const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
            const response = await axios.post(`${API_URL}/analyze`, { 
                poem_text: writing,
                title: title || "Untitled"
            });
        
            onAnalysisReceived(response.data);
            console.log('Analysis received:', response.data);
        } catch (error) {
            console.error('Error getting analysis:', error);
            onAnalysisReceived({ error: error.message });
        } finally {
            setIsLoading(false);
        }
    }

    return <form onSubmit={handleSubmit} className="flex-1 flex flex-col">
        <label htmlFor="title" className="font-bold text-xl text-gray-200 mb-2">Poem Title (optional)</label>
        <input
            id="title"
            type="text"
            className="p-2 mb-4 border rounded-lg bg-gray-200"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Untitled"
        />
        
        <label htmlFor="writing" className="font-bold text-xl text-gray-200 mb-2">Poem Text</label>
        <textarea
            id="writing"
            className="flex-1 p-2 border rounded-lg bg-gray-200 resize-none"
            value={writing}
            onChange={(e) => setWriting(e.target.value)}
            placeholder="Enter your poem here..."
        />
        <button
            type="submit"
            disabled={isLoading}
            className="mt-4 px-4 self-center w-fit py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400"
        >
            {isLoading ? 'Analyzing...' : 'Analyze'}
        </button>
    </form>
}

export default UserInputBox;