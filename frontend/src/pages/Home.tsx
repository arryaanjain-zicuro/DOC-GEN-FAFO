import React from "react";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-800">
      {/* Hero Section */}
      <div className="bg-white py-20 px-6 md:px-12 text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-6 text-blue-700">
          Intelligent Document Transformation Tool
        </h1>
        <p className="max-w-3xl mx-auto text-lg text-gray-600">
          Upload and analyze financial documents like term sheets and agreements.
          Our AI engine extracts structured fields and identifies relationships to help automate document generation.
        </p>
        <div className="mt-8">
          <Link
            to="/parsing-mode"
            className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded shadow-md transition"
          >
            Try Parsing Mode
          </Link>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16 bg-gray-100">
        <div className="max-w-6xl mx-auto px-6 grid md:grid-cols-3 gap-8">
          {[
            {
              title: "Multi-Format Support",
              desc: "Upload DOCX or XLSX files. Parse and preview fields across different document types.",
              icon: "📄",
            },
            {
              title: "AI-Powered Parsing",
              desc: "Leverages structured patterns and Gemini to suggest the most relevant base (alpha) document.",
              icon: "🤖",
            },
            {
              title: "Transformation Ready",
              desc: "Supports document comparison and transformation workflows for generating consistent outputs.",
              icon: "🔁",
            },
          ].map(({ title, desc, icon }) => (
            <div
              key={title}
              className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition"
            >
              <div className="text-4xl mb-4">{icon}</div>
              <h3 className="text-xl font-semibold text-blue-700 mb-2">
                {title}
              </h3>
              <p className="text-gray-600">{desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Call To Action */}
      <div className="bg-blue-600 text-white py-12 text-center px-6">
        <h2 className="text-2xl md:text-3xl font-semibold mb-4">
          Ready to automate your document workflow?
        </h2>
        <p className="mb-6 text-lg">Start by parsing your first document.</p>
        <Link
          to="/parsing-mode"
          className="bg-white text-blue-600 font-semibold py-3 px-6 rounded shadow hover:bg-gray-100 transition"
        >
          Get Started
        </Link>
      </div>
    </div>
  );
}
