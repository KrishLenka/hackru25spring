"use client";

import { useState } from "react";
import InputBox from "@/components/InputBox";
import HighlightedText from "@/components/HighlightedText";
import AnalysisPanel from "@/components/AnalysisPanel";

export default function Home() {
  const [analysis, setAnalysis] = useState<any>(null);

  return (
    <div className="h-screen flex flex-col items-center p-4">
      <h1 className="text-2xl font-bold">AI Political Fact Checker</h1>
      <div className="w-full max-w-4xl flex gap-4 mt-4">
        <div className="w-1/2">
          <InputBox onAnalysis={setAnalysis} />
          {analysis && <HighlightedText text={analysis.source_text} highlights={analysis.highlights || []} />}
        </div>
        <div className="w-1/2">
          {analysis && <AnalysisPanel data={analysis} />}
        </div>
      </div>
    </div>
  );
}
