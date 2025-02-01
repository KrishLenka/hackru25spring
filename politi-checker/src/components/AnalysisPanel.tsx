interface AnalysisPanelProps {
  data: any;
}

const AnalysisPanel: React.FC<AnalysisPanelProps> = ({ data }) => {
  return (
    <div className="p-4 border rounded shadow">
      <h2 className="text-lg font-bold">AI Analysis</h2>
      <p><strong>Extremity:</strong> {data.extremity}/10</p>
      <p><strong>Subjectivity:</strong> {data.subjectivity}/10</p>
      <p><strong>Accuracy:</strong> {data.accuracy}/10</p>
      <h3 className="mt-2 font-bold">Highlighted Terms:</h3>
      <ul>
        {data.highlights && data.highlights.length > 0 ? (
          data.highlights.map((word: string, index: number) => (
            <li key={index} className="bg-red-200 px-1 inline-block m-1 rounded">{word}</li>
          ))
        ) : (
          <p>No specific terms highlighted.</p>
        )}
      </ul>
    </div>
  );
};

export default AnalysisPanel;
