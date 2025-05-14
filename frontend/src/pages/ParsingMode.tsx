import React, { useState } from "react";
import axios from "axios";
import FileUploadField from "../components/FileUploadField";
import ParsedResultCard from "../components/ParsedResultCard";

export default function ParsingMode() {
  const [files, setFiles] = useState<File[]>([]);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (files.length === 0) return;
    setLoading(true);
    const formData = new FormData();
    files.forEach(file => formData.append("files", file));

    try {
      const res = await axios.post("http://localhost:8000/parsing-mode", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data);
    } catch (err) {
      console.error("Upload failed:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-4">
      <h2 className="text-2xl font-semibold">Document Parsing Mode</h2>

      <FileUploadField files={files} setFiles={setFiles} multiple />

      <button
        onClick={handleUpload}
        disabled={loading || files.length === 0}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        {loading ? "Analyzing..." : "Run Parsing"}
      </button>

      {result && (
        <div className="space-y-4 mt-6">
          <h3 className="text-xl font-bold">Summary</h3>
          <p className="text-gray-700 whitespace-pre-wrap">{result.gemini_summary.summary}</p>
          <h4 className="text-lg font-semibold">Suggested Alpha Document: <span className="font-mono">{result.gemini_summary.suggested_alpha}</span></h4>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {result.documents.map((doc: any, i: number) => (
              <ParsedResultCard key={i} document={doc} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
