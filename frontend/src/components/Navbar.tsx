// src/components/Navbar.tsx

//the navbar
import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import SessionStatusButton from "./SessionStatusButton";

const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    localStorage.removeItem("loggedIn");
    navigate("/login");
  };

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="bg-white shadow-md px-6 py-3 flex justify-between items-center">
      <div className="flex gap-4">
        <h1 className="text-lg font-semibold mr-6">Doc Automation Admin</h1>

        <button
          onClick={() => navigate("/")}
          className={`px-3 py-1.5 rounded ${
            isActive("/") ? "bg-blue-600 text-white" : "text-gray-700 hover:bg-gray-100"
          }`}
        >
          Home
        </button>

        <button
          onClick={() => navigate("/parsing-mode")}
          className={`px-3 py-1.5 rounded ${
            isActive("/parsing-mode")
              ? "bg-blue-600 text-white"
              : "text-gray-700 hover:bg-gray-100"
          }`}
        >
          Parsing Mode
        </button>

        <button
          onClick={() => navigate("/pattern-analysis")}
          className={`px-3 py-1.5 rounded ${
            isActive("/pattern-analysis")
              ? "bg-blue-600 text-white"
              : "text-gray-700 hover:bg-gray-100"
          }`}
        >
          Perform Analysis
        </button>
      </div>
      <div className="flex items-center space-x-4">
        <SessionStatusButton />
        {/* your existing Profile button */}
      </div>

      <button
        onClick={handleLogout}
        className="bg-red-500 text-white px-4 py-1.5 rounded hover:bg-red-600"
      >
        Logout
      </button>
    </nav>
  );
};

export default Navbar;
