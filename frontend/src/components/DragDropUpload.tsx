// src/components/DragDropUpload.tsx
import React, { useState, useRef } from "react";
import { X } from "lucide-react";

interface DragDropUploadProps {
  label: string;
  accept: string;
  onFileChange: (file: File | null) => void;
}

const DragDropUpload: React.FC<DragDropUploadProps> = ({ label, accept, onFileChange }) => {
  const [file, setFile] = useState<File | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const newFile = e.dataTransfer.files[0];
    if (newFile && newFile.name.match(accept.replace(".", "\\."))) {
      setFile(newFile);
      onFileChange(newFile);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newFile = e.target.files?.[0] ?? null;
    setFile(newFile);
    onFileChange(newFile);
  };

  const removeFile = () => {
    setFile(null);
    onFileChange(null);
    if (inputRef.current) inputRef.current.value = "";
  };

  return (
    <div className="mb-4">
      <label className="block text-sm font-medium mb-1">{label}</label>
      <div
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        className={`border-2 border-dashed rounded-lg p-4 text-center cursor-pointer ${
          dragOver ? "border-blue-500 bg-blue-50" : "border-gray-300"
        }`}
      >
        {file ? (
          <div className="flex items-center justify-between text-left text-sm text-gray-700">
            <div className="overflow-hidden text-ellipsis whitespace-nowrap w-[85%]">
              📄 {file.name}
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation();
                removeFile();
              }}
              className="text-red-500 hover:text-red-700"
              title="Remove file"
            >
              <X size={16} />
            </button>
          </div>
        ) : (
          <p className="text-sm text-gray-500">Drag & drop or click to upload</p>
        )}
      </div>
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        hidden
        onChange={handleInputChange}
      />
    </div>
  );
};

export default DragDropUpload;
