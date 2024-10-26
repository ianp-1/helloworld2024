// components/BookCard.tsx
import * as React from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

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

interface BookCardProps {
  bookInfo: BookInfo;
}

const BookCard: React.FC<BookCardProps> = ({ bookInfo }) => {
  return (
    <Card className="w-full max-w-lg mb-4">
      <CardHeader>
        <CardTitle>{bookInfo.extracted_title}</CardTitle>
        <CardDescription>Author: {bookInfo.extracted_author}</CardDescription>
      </CardHeader>
      <CardContent>
        {bookInfo.books.map((book, index) => (
          <div key={index} className="mb-4">
            <h3 className="text-md font-bold">{book.title}</h3>
            <p>
              <strong>Author:</strong> {book.author.join(", ")}
            </p>
            <p>
              <strong>First Publish Year:</strong>{" "}
              {book.first_publish_year || "N/A"}
            </p>
            <p>
              <strong>First Sentence:</strong> {book.first_sentence || "N/A"}
            </p>
            <p>
              <strong>Rating Average:</strong> {book.ratings_average || "N/A"}
            </p>
            <p>
              <strong>Rating Count:</strong> {book.ratings_count || "N/A"}
            </p>
          </div>
        ))}
      </CardContent>
      <CardFooter>{/* Optional: Add footer actions if needed */}</CardFooter>
    </Card>
  );
};

export default BookCard;
