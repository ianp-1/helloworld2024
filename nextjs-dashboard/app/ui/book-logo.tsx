import { BookOpenIcon } from "@heroicons/react/24/outline";
import { lusitana } from "@/app/ui/fonts";

export default function BookLogo() {
  return (
    <div
      className={`${lusitana.className} flex flex-row items-center leading-none text-white`}
    >
      <BookOpenIcon className="h-24 w-24" />
      <p className="text-[44px]">Book Review</p>
    </div>
  );
}
