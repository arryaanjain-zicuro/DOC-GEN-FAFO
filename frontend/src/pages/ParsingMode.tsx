import React, { useState } from "react";
import axios from "axios";
import FileUploadField from "../components/FileUploadField";
import ParsedResultCard from "../components/ParsedResultCard";
import DocumentCardList from "../components/DocumentCardList";
import DocumentDetailModal from "../modals/DocumentDetailModal";

export default function ParsingMode() {
  const [files, setFiles] = useState<File[]>([]);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedDoc, setSelectedDoc] = useState<any | null>(null);
  
  const handleDocClick = (doc: any) => {
    setSelectedDoc(doc);
  };

  const handleUpload = async () => {
    if (files.length === 0) return;
    setLoading(true);
    setError(null);
    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));

    try {
      const res = await axios.post(`${import.meta.env.VITE_FAST_API_SERVER}/parsing-mode`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data);
    } catch (err: any) {
      console.error("Upload failed:", err);
      setError("Failed to parse documents. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-6 max-w-5xl mx-auto">
      <h2 className="text-2xl font-semibold text-gray-800">Document Parsing Mode</h2>

      <FileUploadField files={files} setFiles={setFiles} multiple />

      <button
        onClick={handleUpload}
        disabled={loading || files.length === 0}
        className={`px-4 py-2 rounded transition text-white ${
          loading || files.length === 0
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-blue-600 hover:bg-blue-700"
        }`}
      >
        {loading ? "Analyzing..." : "Run Parsing"}
      </button>

      {error && <p className="text-red-500 text-sm">{error}</p>}

      {result && (
        <div className="space-y-6 mt-8">
          <div className="bg-gray-50 p-4 rounded shadow">
            <h3 className="text-xl font-bold text-gray-800">Gemini Summary</h3>
            <p className="text-gray-700 whitespace-pre-wrap mt-2">
              {result.gemini_summary?.summary || "No summary available."}
            </p>
            {result.gemini_summary?.suggested_alpha && (
              <h4 className="text-md mt-4 text-gray-800 font-medium">
                Suggested Alpha Document:{" "}
                <span className="font-mono text-blue-600">
                  {result.gemini_summary.suggested_alpha}
                </span>
              </h4>
            )}
          </div>

          {Array.isArray(result.documents) ? (
            <>
              <DocumentCardList
                documents={result.documents}
                suggestedAlphaId={result.gemini_summary?.suggested_alpha || ""}
                onCardClick={handleDocClick}
              />
              {selectedDoc && (
                <DocumentDetailModal
                  document={selectedDoc}
                  onClose={() => setSelectedDoc(null)}
                />
              )}
            </>
          ) : (
            <p className="text-red-500">Error: Documents are not in expected format.</p>
          )}
        </div>
      )}
    </div>
  );
}
