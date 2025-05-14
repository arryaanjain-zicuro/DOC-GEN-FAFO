import React, { useState } from "react";
import DocumentDetailModal from "../modals/DocumentDetailModal";

interface Document {
  id: string;
  name: string;
  type: string;
  filename: string;
  fields?: any[];
  sheets?: Record<string, any[]>;
}

interface DocumentCardListProps {
  documents: any[];
  suggestedAlphaId: string;
  onCardClick?: (doc: any) => void;
}


const DocumentCardList: React.FC<DocumentCardListProps> = ({
  documents,
  suggestedAlphaId,
  onCardClick, // make sure this is passed
}) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {documents.map((doc) => (
        <div
          key={doc.id}
          onClick={() => onCardClick?.(doc)}
          className="cursor-pointer border border-gray-300 p-4 rounded shadow hover:bg-gray-50 transition"
        >
          <h3 className="text-lg font-semibold">{doc.name || doc.filename}</h3>
          <p className="text-sm text-gray-600">{doc.type.toUpperCase()}</p>

          {suggestedAlphaId === doc.id && (
            <p className="text-green-600 text-sm font-medium mt-1">
              Suggested Alpha
            </p>
          )}

          <p className="mt-2 text-xs text-gray-500">
            {doc.fields?.length || 0} fields extracted
          </p>

          {doc.sheets && (
            <p className="mt-1 text-xs text-gray-500">
              {Object.keys(doc.sheets).length} sheets found
            </p>
          )}
        </div>
      ))}
    </div>
  );
};

export default DocumentCardList;
