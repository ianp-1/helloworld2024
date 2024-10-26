// pages/index.tsx
"use client";
import { useState } from "react";
import FileUploader from "@/app/ui/dashboard/FileUploader";
import BookCard from "@/app/ui/dashboard/BookCard";

interface Book {
  title: string;
  author: string[];
  ratings_average?: number;
  ratings_count?: number;
  first_publish_year?: number;
  first_sentence?: string;
}

interface BookInfo {
  extracted_title: string;
  extracted_author: string;
  books: Book[];
}

export default function HomePage() {
  const [responses, setResponses] = useState<BookInfo[]>([]);

  const handleNewResponse = (newResponses: BookInfo[]) => {
    setResponses((prevResponses) => [...newResponses, ...prevResponses]);
  };

  return (
    <div className="flex flex-col items-center justify-start min-h-screen p-4">
      {/* File Uploader Section */}
      <div className="bg-gray-200 rounded-lg shadow-md p-4 w-full max-w-lg">
        <h1 className="text-lg mb-2 text-center">File Uploader</h1>
        <FileUploader onUploadSuccess={handleNewResponse} />
      </div>

      {/* Display Cards */}
      <div className="w-full max-w-lg mt-4">
        {responses.length === 0 ? (
          <p className="text-center text-gray-500">No uploads yet.</p>
        ) : (
          responses.map((response, index) => (
            <BookCard key={index} bookInfo={response} />
          ))
        )}
      </div>
    </div>
  );
}
