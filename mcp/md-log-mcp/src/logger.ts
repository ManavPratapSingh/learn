import * as fs from "node:fs";
import * as path from "node:path";

export interface QuestionOption {
  label: string;
}

export interface QuizDetails {
  status?: string;
  message?: string;
  dontKnow?: boolean;
  correct?: boolean;
  answers?: Array<{ index: number; label: string }>;
  correctIndices?: number[];
  note?: string;
  explanation?: string;
}

export interface AskDetails {
  status?: string;
  message?: string;
  answers?: Array<{ type?: string; index?: number; label: string }>;
}

export class MdLogger {
  private logFile: string | null = null;
  private writeLock: Promise<void> = Promise.resolve();

  public setLogFile(filepath: string, createIfMissing: boolean = true): string {
    const resolved = path.isAbsolute(filepath)
      ? filepath
      : path.resolve(process.cwd(), filepath);
    const dir = path.dirname(resolved);

    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    if (!fs.existsSync(resolved)) {
      if (createIfMissing) {
        fs.writeFileSync(resolved, "", "utf-8");
      } else {
        throw new Error(`File does not exist: ${resolved}`);
      }
    }

    this.logFile = resolved;

    try {
      const cfg = "/home/manav/learn/.agents/active_frontend_note.json";
      if (!fs.existsSync(path.dirname(cfg))) {
        fs.mkdirSync(path.dirname(cfg), { recursive: true });
      }
      fs.writeFileSync(cfg, JSON.stringify({ filepath: resolved }, null, 2), "utf-8");
    } catch (err) {
      // ignore
    }

    return resolved;
  }

  public stopLogging(): string | null {
    const prev = this.logFile;
    this.logFile = null;
    return prev;
  }

  public getLogFile(): string | null {
    return this.logFile;
  }

  private withLock<T>(fn: () => T | Promise<T>): Promise<T> {
    const prev = this.writeLock;
    let release: () => void;
    this.writeLock = new Promise<void>((r) => {
      release = r;
    });
    return prev.then(fn).finally(() => release!());
  }

  private appendToFile(text: string): void {
    if (!this.logFile) return;
    try {
      let current = "";
      if (fs.existsSync(this.logFile)) {
        current = fs.readFileSync(this.logFile, "utf-8");
      }
      const prefix = current.trim().length > 0 ? "\n\n" : "";
      fs.writeFileSync(this.logFile, current + prefix + text + "\n", "utf-8");
    } catch (err) {
      // File may have been locked or deleted externally
    }
  }

  public formatCallout(type: string, title: string, bodyLines: string[]): string {
    const lines = [`> [!${type}] ${title}`];
    for (const line of bodyLines) {
      lines.push(line.length === 0 ? ">" : `> ${line}`);
    }
    return lines.join("\n");
  }

  public stripSkillBlocks(text: string): string {
    return text.replace(
      /<skill\b([^>]*)>[\s\S]*?<\/skill>/g,
      (_match, attrs: string) => {
        const name = /name="([^"]+)"/.exec(attrs)?.[1];
        return `> [!note] SKILL loaded: ${name ?? "(unknown)"}`;
      },
    );
  }

  public async logUserMessage(text: string): Promise<boolean> {
    if (!this.logFile) return false;
    const trimmed = this.stripSkillBlocks(text.trim());
    if (!trimmed) return false;
    const block = this.formatCallout("quote", "YOU", trimmed.split("\n"));
    await this.withLock(() => this.appendToFile(block));
    return true;
  }

  public async logAssistantMessage(text: string, senderName: string = "ASSISTANT"): Promise<boolean> {
    if (!this.logFile) return false;
    const trimmed = text.trim();
    if (!trimmed) return false;
    const block = this.formatCallout("abstract", senderName, trimmed.split("\n"));
    await this.withLock(() => this.appendToFile(block));
    return true;
  }

  public async logQuestion(
    question: string,
    options: QuestionOption[] = [],
    context?: string,
    label: string = "Question"
  ): Promise<boolean> {
    if (!this.logFile) return false;
    const body: string[] = [];
    for (const line of question.split("\n")) body.push(line);
    if (context) {
      body.push("");
      for (const line of context.split("\n")) body.push(line);
    }
    if (options.length > 0) {
      body.push("");
      body.push(...options.map((o, i) => `${i + 1}. ${o.label}`));
    }
    const block = this.formatCallout("question", label, body);
    await this.withLock(() => this.appendToFile(block));
    return true;
  }

  public async logQuizAnswer(details: QuizDetails): Promise<boolean> {
    if (!this.logFile) return false;
    const status = details?.status;
    let block: string;

    if (status === "cancelled") {
      block = this.formatCallout("warning", "Quiz — cancelled", ["(user skipped)"]);
    } else if (status === "unavailable") {
      block = this.formatCallout("warning", "Quiz — unavailable", [details?.message || ""]);
    } else {
      const dontKnow = details?.dontKnow === true;
      const correct = details?.correct === true;
      const type = dontKnow ? "question" : correct ? "success" : "failure";
      const title = dontKnow
        ? "Quiz — I don't know"
        : correct
          ? "Quiz — correct ✓"
          : "Quiz — incorrect ✗";
      const body: string[] = [];

      if (dontKnow) {
        body.push("Your answer: I don't know");
      } else {
        const answers: any[] = details?.answers || [];
        const sel = answers.map((a) => `${a.index}. ${a.label}`).join(", ") || "(none)";
        body.push(`Your answer: ${sel}`);
      }

      const correctIndices: number[] = details?.correctIndices || [];
      if (correctIndices.length > 0) {
        const correctStr = correctIndices.map((i) => `${i}`).join(", ");
        body.push(`Correct answer: ${correctStr}`);
      }

      if (details?.note) {
        body.push("");
        const noteLines = String(details.note).split("\n");
        body.push(`Note: ${noteLines[0]}`);
        for (let i = 1; i < noteLines.length; i++) body.push(noteLines[i]);
      }

      if (details?.explanation) {
        body.push("");
        for (const line of String(details.explanation).split("\n")) body.push(line);
      }
      block = this.formatCallout(type, title, body);
    }

    await this.withLock(() => this.appendToFile(block));
    return true;
  }

  public async logAskAnswer(details: AskDetails): Promise<boolean> {
    if (!this.logFile) return false;
    const status = details?.status;
    let block: string;

    if (status === "cancelled") {
      block = this.formatCallout("warning", "Question — cancelled", ["(user skipped)"]);
    } else if (status === "unavailable") {
      block = this.formatCallout("warning", "Question — unavailable", [details?.message || ""]);
    } else {
      const answers: any[] = details?.answers || [];
      const body: string[] = answers.map((a) => {
        if (a.type === "other") return `Other: ${a.label}`;
        if (a.type === "text") return a.label;
        return `${a.index !== undefined ? a.index + '. ' : ''}${a.label}`;
      });
      if (body.length === 0) body.push("(no answer)");
      block = this.formatCallout("example", "Answer", body);
    }

    await this.withLock(() => this.appendToFile(block));
    return true;
  }

  public async logCustomEntry(text: string, calloutType?: string, title?: string): Promise<boolean> {
    if (!this.logFile) return false;
    let block: string;
    if (calloutType) {
      block = this.formatCallout(calloutType, title || calloutType.toUpperCase(), text.split("\n"));
    } else {
      block = text;
    }
    await this.withLock(() => this.appendToFile(block));
    return true;
  }
}
