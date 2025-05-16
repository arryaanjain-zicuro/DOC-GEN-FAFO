// src/components/SessionStatusButton.tsx
import React, { useEffect, useState } from "react";
import { LogOut, Database } from "lucide-react";

const SessionStatusButton: React.FC = () => {
  const [sessionId, setSessionId] = useState<string | null>(null);

  useEffect(() => {
    const storedId = localStorage.getItem("session_id");
    if (storedId) {
      setSessionId(storedId);
    }
  }, []);

  const handleClearSession = () => {
    localStorage.removeItem("session_id");
    setSessionId(null);
  };

  if (!sessionId) return null;

  return (
    <div className="flex items-center space-x-3 px-4 py-2 bg-green-100 text-green-800 rounded-md shadow">
      <Database size={16} />
      <span className="text-sm font-medium">Session Active</span>
      <button
        onClick={handleClearSession}
        className="text-xs text-red-500 hover:underline flex items-center"
      >
        <LogOut size={14} className="mr-1" />
        Clear
      </button>
    </div>
  );
};

export default SessionStatusButton;
