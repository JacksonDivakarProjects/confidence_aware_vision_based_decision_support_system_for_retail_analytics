const BASE_URL = "http://127.0.0.1:9000";

export async function fetchInsights() {
  const response = await fetch(`${BASE_URL}/insights`);
  if (!response.ok) {
    throw new Error("Failed to fetch analytics insights");
  }
  return response.json();
}

export async function sendChatQuestion(question) {
  const response = await fetch(`${BASE_URL}/recommendations/chat?question=${encodeURIComponent(question)}`, {
    method: "POST"
  });

  if (!response.ok) {
    throw new Error("Failed to get LLM recommendation");
  }

  return response.json();
}
