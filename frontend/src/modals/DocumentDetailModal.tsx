import React from "react";

interface Field {
  name?: string;
  key?: string;
  value?: string;
  val?: string;
  label?: string;
  content?: string;
  [key: string]: any;
}

interface DocumentDetailModalProps {
  document: {
    id: string;
    name: string;
    type: string;
    filename?: string;
    fields?: Field[];
    sheets?: Record<string, any[]>;
  };
  onClose: () => void;
}

const extractLabelAndValue = (field: Field, idx: number): [string, string] => {
  // Try common label keys
  const label =
    field.name || field.key || field.label || `Field ${idx + 1}`;
  
  // Try common value keys
  const value =
    field.value || field.val || field.content;

  if (value) return [label, value];

  // Fallback: if it's a single-entry object like { "Maturity Date": "2025-01-01" }
  const entries = Object.entries(field);
  if (entries.length === 1) {
    const [rawKey, rawValue] = entries[0];
    return [rawKey, rawValue as string];
  }

  // Fallback for unrecognized shapes
  return [label, ""];
};

const DocumentDetailModal: React.FC<DocumentDetailModalProps> = ({
  document,
  onClose,
}) => {
  if (!document) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded shadow-lg max-w-2xl w-full relative overflow-y-auto max-h-[80vh]">
        <button
          onClick={onClose}
          className="absolute top-2 right-2 text-gray-600 hover:text-red-500 text-xl"
        >
          &times;
        </button>

        <h2 className="text-xl font-bold">
          {document.name || document.filename}
        </h2>
        <p className="text-sm text-gray-600 mb-2">{document.type.toUpperCase()}</p>

        <h3 className="text-md font-semibold mt-4 mb-2">Extracted Fields</h3>
        {document.fields && document.fields.length > 0 ? (
          <ul className="list-disc list-inside text-sm space-y-1">
            {document.fields.map((field, idx) => {
              const [label, value] = extractLabelAndValue(field, idx);
              return (
                <li key={idx}>
                  <strong>{label}:</strong>{" "}
                  {value ? value : <span className="text-gray-400 italic">No value</span>}
                </li>
              );
            })}
          </ul>
        ) : (
          <p className="text-gray-500 text-sm italic">No fields extracted.</p>
        )}

        {document.sheets && (
          <div className="mt-6">
            <h3 className="text-md font-semibold mb-2">Sheet Summary</h3>
            <ul className="list-disc list-inside text-sm space-y-1">
              {Object.entries(document.sheets).map(([sheet, rows]) => (
                <li key={sheet}>
                  <strong>{sheet}</strong>: {rows.length} rows
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default DocumentDetailModal;
