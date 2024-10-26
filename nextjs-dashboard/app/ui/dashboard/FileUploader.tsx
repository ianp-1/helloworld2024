// components/FileUploader.tsx
"use client";

import { useState } from "react";

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

interface FileUploaderProps {
  onUploadSuccess: (data: BookInfo[]) => void;
}

const FileUploader: React.FC<FileUploaderProps> = ({ onUploadSuccess }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string>("");
  const [responseData, setResponseData] = useState<any>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadStatus("Please select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setUploadStatus("Uploading...");
      const response = await fetch("http://127.0.0.1:5000/process-image", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setResponseData(data);
        setUploadStatus("Upload successful!");

        if (data.books_info && data.books_info.length > 0) {
          // Filter out entries with empty books array
          const validBookInfos = data.books_info.filter(
            (info: BookInfo) => info.books.length > 0
          );
          onUploadSuccess(validBookInfos);
        }
      } else {
        setUploadStatus("Upload failed.");
      }
    } catch (error) {
      setUploadStatus("Error uploading file.");
      console.error("Upload error:", error);
    }
  };

  return (
    <div>
      <h2 className="text-md font-semibold mb-2">Image Uploader</h2>
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="mb-2"
      />
      <button
        onClick={handleUpload}
        className="mt-2 px-4 py-2 bg-blue-500 text-white rounded"
      >
        Upload Image
      </button>
      <p className="mt-2">{uploadStatus}</p>

      {responseData && (
        <div className="mt-4">
          <h3 className="text-md font-semibold">Extracted Text:</h3>
          <p>{responseData.extracted_text}</p>

          {/* Optional: Display raw books_info */}
          <h3 className="text-md font-semibold mt-2">Books Info:</h3>
          {responseData.books_info?.map((book: any, index: number) => (
            <div key={index} className="mb-4">
              <h4 className="font-semibold">Book {index + 1}</h4>
              <p>
                <strong>Extracted Title:</strong> {book.extracted_title}
              </p>
              <p>
                <strong>Extracted Author:</strong> {book.extracted_author}
              </p>

              {book.books?.map((info: any, i: number) => (
                <div key={i} className="ml-4">
                  <p>
                    <strong>Title:</strong> {info.title}
                  </p>
                  <p>
                    <strong>Author:</strong> {info.author.join(", ")}
                  </p>
                  <p>
                    <strong>First Publish Year:</strong>{" "}
                    {info.first_publish_year || "N/A"}
                  </p>
                  <p>
                    <strong>First Sentence:</strong>{" "}
                    {info.first_sentence || "N/A"}
                  </p>
                  <p>
                    <strong>Rating Average:</strong>{" "}
                    {info.ratings_average || "N/A"}
                  </p>
                  <p>
                    <strong>Rating Count:</strong> {info.ratings_count || "N/A"}
                  </p>
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FileUploader;
