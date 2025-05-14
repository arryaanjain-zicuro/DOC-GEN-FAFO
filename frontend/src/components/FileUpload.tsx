// src/components/FileUpload.tsx
import React from "react";

interface FileUploadProps {
  label: string;
  accept: string;
  onFileChange: (file: File | null) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ label, accept, onFileChange }) => {
  return (
    <div className="flex flex-col gap-2 mb-4">
      <label className="text-sm font-medium">{label}</label>
      <input
        type="file"
        accept={accept}
        onChange={(e) => onFileChange(e.target.files?.[0] ?? null)}
        className="block w-full text-sm text-gray-700 file:mr-4 file:py-2 file:px-4
                   file:rounded-md file:border-0 file:text-sm file:font-semibold
                   file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
      />
    </div>
  );
};

export default FileUpload;
