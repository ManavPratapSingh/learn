export interface AskOptionInput {
  label: string;
  value?: string;
  description?: string;
}

export interface AskOption {
  label: string;
  value: string;
  description?: string;
}

export interface TextAnswer {
  type: "text";
  label: string;
  value: string;
}

export interface OptionAnswer {
  type: "option";
  label: string;
  value: string;
  index: number;
}

export interface OtherAnswer {
  type: "other";
  label: string;
  value: string;
}

export type AskAnswer = TextAnswer | OptionAnswer | OtherAnswer;

export interface AskQuestionResult {
  status: "answered" | "cancelled" | "unavailable";
  question: string;
  context?: string;
  mode: "text" | "single-select" | "multi-select";
  options: AskOption[];
  answers: AskAnswer[];
  formattedOutput: string;
}

export function normalizeOptions(options?: AskOptionInput[]): AskOption[] {
  return (options || [])
    .map((option) => ({
      label: option.label.trim(),
      value: option.value?.trim() || option.label.trim(),
      description: option.description?.trim() || undefined,
    }))
    .filter((option) => option.label.length > 0);
}

export function getOtherLabel(options: AskOption[]): string {
  return options.some((option) => option.label.toLowerCase() === "other")
    ? "Other (custom)"
    : "Other";
}

export function processQuestion(params: {
  question: string;
  details?: string;
  options?: AskOptionInput[];
  multiSelect?: boolean;
  selectedAnswers?: Array<{ value?: string; index?: number; text?: string; type?: "option" | "other" | "text" }>;
  otherText?: string;
  textResponse?: string;
}): AskQuestionResult {
  const options = normalizeOptions(params.options);
  const context = params.details?.trim() || undefined;
  const mode: "text" | "single-select" | "multi-select" =
    options.length === 0 ? "text" : params.multiSelect ? "multi-select" : "single-select";

  const answers: AskAnswer[] = [];

  if (mode === "text") {
    const text = params.textResponse || (params.selectedAnswers?.[0]?.text) || "";
    const trimmed = text.trim();
    answers.push({
      type: "text",
      label: trimmed,
      value: trimmed,
    });
  } else {
    const otherLabel = getOtherLabel(options);

    if (params.otherText && params.otherText.trim().length > 0) {
      const oText = params.otherText.trim();
      answers.push({
        type: "other",
        label: oText,
        value: oText,
      });
    }

    if (params.selectedAnswers) {
      for (const sa of params.selectedAnswers) {
        if (sa.type === "other" && sa.text) {
          answers.push({ type: "other", label: sa.text.trim(), value: sa.text.trim() });
        } else if (sa.index !== undefined && sa.index > 0 && sa.index <= options.length) {
          const opt = options[sa.index - 1];
          answers.push({
            type: "option",
            label: opt.label,
            value: opt.value,
            index: sa.index,
          });
        } else if (sa.value) {
          const idx = options.findIndex((o) => o.value === sa.value || o.label === sa.value);
          if (idx !== -1) {
            answers.push({
              type: "option",
              label: options[idx].label,
              value: options[idx].value,
              index: idx + 1,
            });
          }
        }
      }
    }
  }

  // Format response string for the model
  const lines: string[] = [];
  lines.push(`Question: ${params.question}`);
  if (context) {
    lines.push(`Context: ${context}`);
  }
  lines.push(`Mode: ${mode}`);
  lines.push("");

  if (options.length > 0) {
    lines.push("Available Options:");
    options.forEach((opt, idx) => {
      lines.push(`  ${idx + 1}. ${opt.label}${opt.description ? ` (${opt.description})` : ""}`);
    });
    lines.push(`  - ${getOtherLabel(options)} (custom text write-in)`);
    lines.push("");
  }

  if (answers.length === 0) {
    lines.push("Status: Awaiting user response.");
  } else {
    lines.push("User Answers:");
    answers.forEach((ans) => {
      if (ans.type === "text") {
        lines.push(`  - Answer: ${ans.label.length > 0 ? ans.label : "(empty)"}`);
      } else if (ans.type === "other") {
        lines.push(`  - Other (custom): ${ans.label}`);
      } else {
        lines.push(`  - ${ans.index}. ${ans.label}`);
      }
    });
  }

  return {
    status: "answered",
    question: params.question,
    context,
    mode,
    options,
    answers,
    formattedOutput: lines.join("\n"),
  };
}
