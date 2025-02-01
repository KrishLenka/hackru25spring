import { useState } from "react";
import { factCheckText, factCheckLink } from "@/utils/api";

interface InputBoxProps {
  onAnalysis: (data: any) => void;
}

const InputBox: React.FC<InputBoxProps> = ({ onAnalysis }) => {
  const [input, setInput] = useState("");
  const [isURL, setIsURL] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!input.trim()) return;
    setLoading(true);

    try {
      const data = isURL ? await factCheckLink(input) : await factCheckText(input);
      if (data) {
        onAnalysis(data); // Send the API response to the parent component
      }
    } catch (error) {
      console.error("API Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <textarea 
        className="w-full border p-2 rounded"
        rows={4}
        placeholder="Enter text or URL..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <div className="flex gap-4 mt-2">
        <button onClick={() => setIsURL(!isURL)} className="bg-gray-300 px-4 py-1 rounded">
          {isURL ? "Switch to Text" : "Switch to URL"}
        </button>
        <button onClick={handleSubmit} className="bg-blue-500 text-white px-4 py-1 rounded">
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </div>
    </div>
  );
};

export default InputBox;
