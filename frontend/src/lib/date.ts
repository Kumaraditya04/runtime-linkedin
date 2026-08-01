/**
 * Universal Date Formatter for Indian Standard Time (IST / Asia/Kolkata).
 * Automatically handles UTC ISO strings with/without 'Z' or offset to ensure +05:30 conversion.
 */
export function formatIST(dateStr: string | null | undefined, includeTime = true): string {
  if (!dateStr) return "-";
  try {
    let s = String(dateStr).trim();
    if (s.includes(" ") && !s.includes("T")) {
      s = s.replace(" ", "T");
    }
    if (!s.endsWith("Z") && !s.includes("+")) {
      s += "Z";
    }
    const date = new Date(s);
    if (isNaN(date.getTime())) return "-";

    if (includeTime) {
      return date.toLocaleString("en-IN", {
        timeZone: "Asia/Kolkata",
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        hour12: true,
      });
    }
    return date.toLocaleDateString("en-IN", {
      timeZone: "Asia/Kolkata",
      day: "2-digit",
      month: "short",
      year: "numeric",
    });
  } catch (e) {
    return "-";
  }
}
