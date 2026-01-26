import { useState } from 'react';
import UserInputBox from './components/UserInputBox';
import AnalysisOutputBox from './components/AnalysisOutputBox';

const App = () => {
    const [analysisResult, setAnalysisResult] = useState(null);
    
    return <div className="flex flex-col min-h-screen">
        <header className="bg-gray-800 text-white p-4">
            <h1 className="text-2xl font-bold text-center">Oracle of the Abyss</h1>
        </header>
        <div className="flex flex-1 justify-between gap-4 p-4">
            <UserInputBox onAnalysisReceived={setAnalysisResult} />
            <AnalysisOutputBox analysisResult={analysisResult} />
        </div>
    </div>
}
 
export default App;