import React from "react";

interface Props {
  files: File[];
  setFiles: (files: File[]) => void;
  multiple?: boolean;
}

export default function FileUploadField({ files, setFiles, multiple = false }: Props) {
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
    <div className="space-y-2">
      <input
        type="file"
        accept=".docx,.xlsx"
        multiple={multiple}
        onChange={handleChange}
        className="block"
      />

      <ul className="text-sm text-gray-700">
        {files.map((file, index) => (
          <li key={index} className="flex justify-between items-center">
            <span>{file.name}</span>
            <button
              onClick={() => removeFile(index)}
              className="text-red-500 text-xs hover:underline"
            >
              Remove
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
