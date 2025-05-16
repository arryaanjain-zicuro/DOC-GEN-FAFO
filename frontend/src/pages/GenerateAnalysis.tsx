// src/pages/GenerateAnalysis.tsx
import React, { useState } from "react";
import axios from "axios";
import DragDropUpload from "../components/DragDropUpload";

const GenerateAnalysis: React.FC = () => {
  const [alphaFile, setAlphaFile] = useState<File | null>(null);
  const [betaDocFile, setBetaDocFile] = useState<File | null>(null);
  const [betaExcelFile, setBetaExcelFile] = useState<File | null>(null);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [elapsedTime, setElapsedTime] = useState<number | null>(null);



  const handleSubmit = async () => {
    if (!alphaFile || !betaDocFile || !betaExcelFile) {
      alert("Please upload all required files.");
      return;
    }
  
    setIsLoading(true);
    setElapsedTime(null); // Reset timer display
  
    const startTime = performance.now(); // More accurate than Date.now()
    const formData = new FormData();
    formData.append("alpha_doc", alphaFile);
    formData.append("beta_word_doc", betaDocFile);
    formData.append("beta_excel_doc", betaExcelFile);
  
    try {
      const response = await axios.post(`${import.meta.env.VITE_FAST_API_SERVER}/run-transformation`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      const endTime = performance.now();
      setElapsedTime(((endTime - startTime) / 1000));
      setAnalysisResult(response.data);
      // ✅ Save session_id to localStorage
      if (response.data.session_id) {
        localStorage.setItem("session_id", response.data.session_id);
      }
    } catch (error) {
      console.error("Error running transformation:", error);
      alert("Failed to process documents.");
    } finally {
      setIsLoading(false);
    }
  };
  
  

  return (
    <div className="max-w-5xl mx-auto mt-8 p-6 bg-white shadow-md rounded-lg">
      <h2 className="text-2xl font-bold mb-6 text-center">Generate Document Analysis</h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <DragDropUpload label="Alpha Document (.docx)" accept=".docx" onFileChange={setAlphaFile} />
        <DragDropUpload label="Beta Request Letter (.docx)" accept=".docx" onFileChange={setBetaDocFile} />
        <DragDropUpload label="Beta MIS Excel (.xlsx)" accept=".xlsx" onFileChange={setBetaExcelFile} />
      </div>

      <button
      onClick={handleSubmit}
      disabled={isLoading || !alphaFile || !betaDocFile || !betaExcelFile}
      className={`w-full mt-6 py-2 rounded text-white transition ${
        isLoading || !alphaFile || !betaDocFile || !betaExcelFile
          ? "bg-gray-400 cursor-not-allowed"
          : "bg-blue-600 hover:bg-blue-700"
        }`}
      >
        {isLoading ? "Processing..." : "Submit for Pattern Analysis"}
      </button>

      {elapsedTime !== null && (
        <p className="mt-2 text-center text-sm text-gray-600">
          Analysis completed in <span className="font-medium">{elapsedTime.toFixed(2)}</span> seconds.
        </p>
      )}

      {analysisResult && (
        <div className="mt-10">
          {/* Alpha Fields */}
          <section className="mb-6">
            <h3 className="text-xl font-semibold mb-2">Alpha Document Fields</h3>
            <ul className="list-disc ml-5 max-h-48 overflow-y-auto">
              {analysisResult.state.alpha_data.inferred_fields.slice(0, 20).map((field: any, idx: number) => (
                <li key={idx}>{field.name}</li>
              ))}
            </ul>
          </section>

          {/* Beta Excel Mapping */}
          <section className="mb-6">
            <h3 className="text-xl font-semibold mb-2">Beta Excel Analysis</h3>
            <p className="text-gray-700 mb-2">Transformation Notes: <i>{analysisResult.state.beta_excel_data.transformation_notes}</i></p>
            <p className="mb-2">Unmatched cells: {analysisResult.state.beta_excel_data.unmatched_beta_cells.length}</p>
            <table className="w-full text-sm border border-gray-300">
              <thead>
                <tr className="bg-gray-100">
                  <th className="border px-2 py-1">Alpha Field</th>
                  <th className="border px-2 py-1">Sheet</th>
                  <th className="border px-2 py-1">Cell</th>
                  <th className="border px-2 py-1">Value</th>
                  <th className="border px-2 py-1">Action</th>
                  <th className="border px-2 py-1">Explanation</th>
                </tr>
              </thead>
              <tbody>
                {analysisResult.state.beta_excel_data.field_mappings.slice(0, 5).map((map: any, idx: number) => (
                  <tr key={idx}>
                    <td className="border px-2 py-1">{map.alpha_field}</td>
                    <td className="border px-2 py-1">{map.sheet}</td>
                    <td className="border px-2 py-1">{map.cell}</td>
                    <td className="border px-2 py-1">{map.value}</td>
                    <td className="border px-2 py-1">{map.action}</td>
                    <td className="border px-2 py-1">{map.explanation}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>

          {/* Beta Word Analysis */}
         {/* Beta Word Mappings */}
          <section className="mb-6">
            <h3 className="text-xl font-semibold mb-2">Beta Word Field Mappings</h3>
            <table className="w-full text-sm border border-gray-300">
              <thead>
                <tr className="bg-gray-100">
                  <th className="border px-2 py-1">Alpha Field</th>
                  <th className="border px-2 py-1">Matched Text</th>
                  <th className="border px-2 py-1">Action</th>
                  <th className="border px-2 py-1">Explanation</th>
                </tr>
              </thead>
              <tbody>
                {analysisResult.state.beta_word_data.field_mappings.slice(0, 5).map((map: any, idx: number) => (
                  <tr key={idx}>
                    <td className="border px-2 py-1">{map.alpha_field}</td>
                    <td className="border px-2 py-1">{map.matched_text}</td>
                    <td className="border px-2 py-1">{map.action}</td>
                    <td className="border px-2 py-1">{map.explanation}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>

        </div>
      )}
    </div>
  );
};

export default GenerateAnalysis;
