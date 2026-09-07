export interface QuizOptionInput {
  label: string;
  value?: string;
  description?: string;
}

export interface QuizOption {
  label: string;
  value: string;
  description?: string;
}

export interface DisplayedOption {
  index: number; // 1-based index in display order
  label: string;
  value: string;
  description?: string;
}

export interface QuizEvaluationResult {
  status: "answered" | "cancelled" | "unavailable";
  question: string;
  context?: string;
  mode: "single-select" | "multi-select";
  options: DisplayedOption[];
  correctIndices: number[]; // 1-based display indices
  selectedIndices: number[]; // 1-based display indices
  selectedValues: string[];
  correctValues: string[];
  isCorrect: boolean;
  dontKnow: boolean;
  explanation: string;
  formattedOutput: string;
  userNote?: string;
}

export function normalizeOptions(options?: QuizOptionInput[]): QuizOption[] {
  if (!options || options.length < 2) {
    throw new Error("Quiz requires at least two options.");
  }
  const seen = new Set<string>();
  return options
    .map((opt) => ({
      label: opt.label.trim(),
      value: opt.value?.trim() || opt.label.trim(),
      description: opt.description?.trim() || undefined,
    }))
    .filter((opt) => {
      if (opt.label.length === 0) return false;
      if (seen.has(opt.value)) {
        throw new Error(`Duplicate option value "${opt.value}"`);
      }
      seen.add(opt.value);
      return true;
    });
}

export function shuffleOptions<T>(arr: T[]): T[] {
  const out = [...arr];
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

export function coerceCorrectAnswer(correctAnswer: string | string[]): string[] {
  if (Array.isArray(correctAnswer)) return correctAnswer;
  const trimmed = correctAnswer.trim();
  if (trimmed.startsWith("[") && trimmed.endsWith("]")) {
    try {
      const parsed = JSON.parse(trimmed);
      if (Array.isArray(parsed)) return parsed.map((v) => String(v));
    } catch {
      // Treat as literal string value
    }
  }
  return [correctAnswer];
}

export function resolveCorrect(
  correctAnswer: string | string[],
  options: QuizOption[]
): { correctIndices: number[]; correctValues: string[] } {
  const arr = coerceCorrectAnswer(correctAnswer);
  if (arr.length === 0) {
    throw new Error("correctAnswer parameter is required.");
  }

  const byValue = new Map(options.map((o, i) => [o.value, i + 1]));
  const indices: number[] = [];
  const validValues: string[] = [];

  for (const raw of arr) {
    const v = typeof raw === "string" ? raw.trim() : String(raw);
    const idx = byValue.get(v);
    if (idx === undefined) {
      const known = options.map((o) => `"${o.value}"`).join(", ");
      throw new Error(`correctAnswer "${v}" does not match any option value (${known})`);
    }
    indices.push(idx);
    validValues.push(v);
  }

  return {
    correctIndices: Array.from(new Set(indices)).sort((a, b) => a - b),
    correctValues: validValues,
  };
}

export function checkCorrect(selectedIndices: number[], correctIndices: number[]): boolean {
  if (selectedIndices.length !== correctIndices.length) return false;
  const a = [...selectedIndices].sort((x, y) => x - y);
  const b = [...correctIndices].sort((x, y) => x - y);
  return a.every((val, idx) => val === b[idx]);
}

export function gradeQuiz(params: {
  question: string;
  options: QuizOptionInput[];
  correctAnswer: string | string[];
  explanation: string;
  details?: string;
  multiSelect?: boolean;
  shuffle?: boolean;
  selectedValues?: string[];
  selectedIndices?: number[];
  dontKnow?: boolean;
  userNote?: string;
}): QuizEvaluationResult {
  const mode = params.multiSelect ? "multi-select" : "single-select";
  let options = normalizeOptions(params.options);

  if (params.shuffle !== false) {
    options = shuffleOptions(options);
  }

  const displayedOptions: DisplayedOption[] = options.map((o, i) => ({
    index: i + 1,
    label: o.label,
    value: o.value,
    description: o.description,
  }));

  const { correctIndices, correctValues } = resolveCorrect(params.correctAnswer, options);

  const dontKnow = params.dontKnow === true;
  let selectedIndices: number[] = [];
  let selectedValues: string[] = [];

  if (!dontKnow) {
    if (params.selectedIndices && params.selectedIndices.length > 0) {
      selectedIndices = params.selectedIndices;
      selectedValues = selectedIndices.map((idx) => {
        const opt = displayedOptions.find((o) => o.index === idx);
        return opt ? opt.value : "";
      }).filter((v) => v.length > 0);
    } else if (params.selectedValues && params.selectedValues.length > 0) {
      selectedValues = params.selectedValues;
      selectedIndices = selectedValues.map((val) => {
        const opt = displayedOptions.find((o) => o.value === val);
        return opt ? opt.index : 0;
      }).filter((idx) => idx > 0);
    }
  }

  const isCorrect = dontKnow ? false : checkCorrect(selectedIndices, correctIndices);

  // Build human-readable formatted feedback
  const lines: string[] = [];
  lines.push(`Question: ${params.question}`);
  if (params.details) {
    lines.push(`Context: ${params.details}`);
  }
  lines.push(`Mode: ${mode}`);
  lines.push("");
  lines.push("Options:");

  const correctSet = new Set(correctIndices);
  const selectedSet = new Set(selectedIndices);

  for (const opt of displayedOptions) {
    const isSel = selectedSet.has(opt.index);
    const isKey = correctSet.has(opt.index);

    let mark = "  ";
    if (dontKnow) {
      mark = isKey ? "✓ " : "  ";
    } else if (isSel && isKey) {
      mark = "✓ ";
    } else if (isSel && !isKey) {
      mark = "✗ ";
    } else if (!isSel && isKey) {
      mark = "✓ ";
    }

    lines.push(`${mark}${opt.index}. ${opt.label} (value: "${opt.value}")`);
    if (opt.description) {
      lines.push(`   ${opt.description}`);
    }
  }

  lines.push("");
  if (dontKnow) {
    lines.push("User Verdict: Selected \"I don't know\" (genuine knowledge gap)");
  } else if (isCorrect) {
    lines.push("User Verdict: ✓ Correct!");
  } else {
    lines.push("User Verdict: ✗ Incorrect.");
  }

  const correctDisplay = correctIndices
    .map((idx) => {
      const o = displayedOptions.find((opt) => opt.index === idx);
      return `${idx}. ${o ? o.label : ""}`;
    })
    .join(", ");
  lines.push(`Correct Answer(s): ${correctDisplay}`);

  if (params.userNote) {
    lines.push(`User Note: ${params.userNote}`);
  }

  lines.push("");
  lines.push(`Explanation: ${params.explanation}`);

  return {
    status: "answered",
    question: params.question,
    context: params.details,
    mode,
    options: displayedOptions,
    correctIndices,
    selectedIndices,
    selectedValues,
    correctValues,
    isCorrect,
    dontKnow,
    explanation: params.explanation,
    userNote: params.userNote,
    formattedOutput: lines.join("\n"),
  };
}
