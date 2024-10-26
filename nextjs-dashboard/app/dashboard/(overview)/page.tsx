"use client"; // Add this directive to indicate that this is a client component

import { useEffect, useState } from 'react';
import FileUploader from "@/app/ui/dashboard/FileUploader";

// Define a type for the book response
interface Book {
  key: string;
  title: string;
  ratings_average?: number; // Optional property
}

export default function HomePage() {
  const [ratingsAverage, setRatingsAverage] = useState<number | null>(null); // State for ratings average
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null); // Set error type to string or null
  const [showRatings, setShowRatings] = useState(false); // State to control when to show ratings

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/search?query=harry%20potter'); // Your Flask API URL
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log('API Response:', data); // Log the full response for debugging

        if (data.docs && data.docs.length > 0) {
          const firstBook: Book = data.docs[0];
          setRatingsAverage(firstBook.ratings_average || null); // Set ratings average
          console.log('First Book Ratings Average:', firstBook.ratings_average); // Log the rating
        } else {
          console.log('No books found.');
        }
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message); // Handle known error types
        } else {
          setError('An unknown error occurred'); // Fallback error message
        }
      } finally {
        setLoading(false); // Set loading to false after fetching
        setShowRatings(true); // Show ratings after fetching
      }
    };

    fetchBooks(); // Call the fetch function
  }, []);

  // Render logic
  return (
    <div className="flex flex-col items-center justify-top min-h-screen p-4">
      <div className="bg-gray-200 rounded-lg shadow-md p-4 w-full max-w-lg">
        <h1 className="text-lg mb-2 text-center">File Uploader</h1>
        <FileUploader />
      </div>
      <div className="mt-4 bg-gray-200 rounded-lg shadow-md p-4 w-full max-w-lg">
        <h1 className="text-lg mb-2 text-center">Book Ratings</h1>
        {loading && <p>Loading...</p>}
        {error && <p>Error: {error}</p>}
        {showRatings && ratingsAverage !== null ? (
          <p className="text-center">The average rating for the first book is: {ratingsAverage}</p>
        ) : (
          showRatings && <p className="text-center">No ratings available for the book.</p>
        )}
      </div>
    </div>
  );
}
