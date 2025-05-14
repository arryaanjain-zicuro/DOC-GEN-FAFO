import React from "react";

export default function ParsedResultCard({ document }: { document: any }) {
  return (
    <div className="p-4 border rounded-lg shadow-sm bg-white">
      <h4 className="font-semibold text-lg mb-2">{document.filename}</h4>
      <p className="text-xs mb-1">Type: {document.type}</p>

      {document.fields && (
        <div className="space-y-1 text-sm">
          <p className="font-medium">Extracted Fields:</p>
          <ul className="list-disc list-inside">
            {document.fields.map((field: any, idx: number) => (
              <li key={idx}>{JSON.stringify(field)}</li>
            ))}
          </ul>
        </div>
      )}

      {document.sheets && (
        <div className="text-sm mt-2">
          <p className="font-medium">Sheet Summary:</p>
          <ul className="list-disc list-inside">
            {Object.entries(document.sheets).map(([sheet, rows]: any) => (
              <li key={sheet}>{sheet}: {rows.length} rows</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
