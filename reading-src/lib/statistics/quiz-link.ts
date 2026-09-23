/** Build a chapter-specific ChatGPT link with a quiz request. */
export function quizLink(title: string, chapterPath: string): string {
  const chapterUrl = new URL(chapterPath, 'https://june.kim').href;
  const prompt = `Read ${chapterUrl} before quizzing me on "${title}". Use the chapter's examples and terminology. Ask five questions, one question at a time: two conceptual multiple-choice questions, one interpretation of an experiment or diagram, one short explanation, and one new application. Wait for my answer before giving specific feedback and explaining the reasoning. Do not reveal later answers. After the fifth question, briefly tell me what to revisit. Start with question 1.`;
  return `https://chatgpt.com/?q=${encodeURIComponent(prompt)}`;
}
