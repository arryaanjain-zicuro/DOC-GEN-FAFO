import React from "react";
import { Upload, FileText, X } from "lucide-react";

interface Props {
  files: File[];
  setFiles: (files: File[]) => void;
  multiple?: boolean;
}

const FileUploadField: React.FC<Props> = ({ files, setFiles, multiple = false }) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const newFiles = Array.from(e.target.files);
      setFiles(multiple ? [...files, ...newFiles] : newFiles);
    }
  };

  const removeFile = (index: number) => {
    const updated = files.filter((_, i) => i !== index);
    setFiles(updated);
  };

  return (
    <div className="w-full">
      <label htmlFor="file-upload">
        <div className="flex items-center gap-2 cursor-pointer px-4 py-2 bg-blue-500 text-white text-sm rounded hover:bg-blue-600 transition w-fit">
          <Upload size={16} />
          Choose {multiple ? "Files" : "File"}
        </div>
      </label>

      <input
        id="file-upload"
        type="file"
        accept=".docx,.xlsx"
        multiple={multiple}
        onChange={handleChange}
        className="hidden"
      />

      <div className="mt-3 space-y-2">
        {files.length === 0 ? (
          <p className="text-sm text-gray-500">No file chosen</p>
        ) : (
          files.map((file, index) => (
            <div
              key={index}
              className="flex items-center justify-between bg-gray-100 px-3 py-2 rounded text-sm"
            >
              <div className="flex items-center gap-2 truncate">
                <FileText size={16} className="text-blue-500" />
                <span className="truncate max-w-xs">{file.name}</span>
              </div>
              <button
                type="button"
                onClick={() => removeFile(index)}
                className="text-red-500 hover:text-red-600"
              >
                <X size={16} />
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default FileUploadField;
