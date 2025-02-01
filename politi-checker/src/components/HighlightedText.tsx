interface HighlightedTextProps {
  text: string;
  highlights: string[];
}

const HighlightedText: React.FC<HighlightedTextProps> = ({ text, highlights }) => {
  if (!text) return null;

  // Split text into words and apply highlights
  const words = text.split(/\s+/).map((word, index) => {
    const isHighlighted = highlights.includes(word);
    return (
      <span 
        key={index} 
        className={isHighlighted ? "bg-yellow-300 px-1 rounded" : ""}
      >
        {word}{" "}
      </span>
    );
  });

  return <div className="p-4 border">{words}</div>;
};

export default HighlightedText;
