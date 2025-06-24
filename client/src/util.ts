import { format, parseISO } from "date-fns";

const formatTimestamp = (timestamp: string) => {
    try {
      const date = parseISO(timestamp);
      return format(date, "MMM d, h:mm a");
    } catch {
      return timestamp; // fallback to original if parsing fails
    }
  };

export { formatTimestamp };