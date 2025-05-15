// src/pages/GenerateAnalysis.tsx
import React, { useState } from "react";
import DragDropUpload from "../components/DragDropUpload";

const GenerateAnalysis: React.FC = () => {
  const [alphaFile, setAlphaFile] = useState<File | null>(null);
  const [betaDocFile, setBetaDocFile] = useState<File | null>(null);
  const [betaExcelFile, setBetaExcelFile] = useState<File | null>(null);

  const handleSubmit = () => {
    if (!alphaFile || !betaDocFile || !betaExcelFile) {
      alert("Please upload all required files.");
      return;
    }
    console.log({ alphaFile, betaDocFile, betaExcelFile });
  };

  return (
    <>
      <div className="max-w-xl mx-auto mt-8 p-6 bg-white shadow-md rounded-lg">
        <h2 className="text-xl font-bold mb-6 text-center">Upload Documents for Training</h2>

        <DragDropUpload label="Alpha Document (.docx)" accept=".docx" onFileChange={setAlphaFile} />
        <DragDropUpload label="Beta Request Letter (.docx)" accept=".docx" onFileChange={setBetaDocFile} />
        <DragDropUpload label="Beta MIS Excel (.xlsx)" accept=".xlsx" onFileChange={setBetaExcelFile} />

        <button
          onClick={handleSubmit}
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          Submit for Pattern Analysis
        </button>
      </div>
    </>
  );
};

export default GenerateAnalysis;
