const AnalysisOutputBox = ({ analysisResult }) => {
    const formatAnalysis = () => {
        if (!analysisResult) return '';
        
        if (analysisResult.error) {
            return `Error: ${analysisResult.error}`;
        }

        const { stanza_texts, line_counts, syllables_per_line } = analysisResult;
        
        if (!stanza_texts) return '';

        let output = '';
        
        for (let i = 0; i < stanza_texts.length; i++) {
            output += `Stanza ${i + 1}:\n`;
            output += `${stanza_texts[i]}\n\n`;
            output += `Lines: ${line_counts[i]}\n`;
            output += `Syllables per line: ${syllables_per_line[i].join(', ')}\n`;
            output += '\n' + '─'.repeat(50) + '\n\n';
        }
        
        return output;
    };

    return <div className="flex-1 flex flex-col">
        <label htmlFor="analysis" className="font-bold text-xl text-gray-200 mb-2">Analysis Result</label>
        <textarea
            id="analysis"
            className="flex-1 p-2 border rounded-lg bg-gray-200 resize-none font-mono"
            value={formatAnalysis()}
            readOnly
        />
    </div>
}

export default AnalysisOutputBox;