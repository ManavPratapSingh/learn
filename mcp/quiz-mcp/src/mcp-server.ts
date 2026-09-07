import * as readline from "node:readline";
import { gradeQuiz, QuizOptionInput } from "./quiz-engine.js";

export class QuizMcpServer {
  public start() {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
      terminal: false,
    });

    rl.on("line", (line: string) => {
      const trimmed = line.trim();
      if (!trimmed) return;

      try {
        const message = JSON.parse(trimmed);
        this.handleMessage(message);
      } catch (err) {
        this.sendError(null, -32700, "Parse error", String(err));
      }
    });

    process.stderr.write("quiz MCP Server started on stdio\n");
  }

  private handleMessage(msg: any) {
    if (!msg || typeof msg !== "object") return;

    if (msg.id === undefined || msg.id === null) {
      if (msg.method === "notifications/initialized") {
        // Handshake acknowledged
      }
      return;
    }

    const { id, method, params } = msg;

    switch (method) {
      case "initialize":
        this.sendResult(id, {
          protocolVersion: "2024-11-05",
          capabilities: { tools: {} },
          serverInfo: { name: "quiz-mcp", version: "1.0.0" },
        });
        break;

      case "tools/list":
        this.sendResult(id, {
          tools: this.getToolDefinitions(),
        });
        break;

      case "tools/call":
        this.handleToolCall(id, params?.name, params?.arguments || {});
        break;

      case "ping":
        this.sendResult(id, {});
        break;

      default:
        this.sendError(id, -32601, `Method not found: ${method}`);
        break;
    }
  }

  private getToolDefinitions() {
    return [
      {
        name: "quiz",
        description:
          "Ask the user a GRADED question with a known correct answer, then instantly grade and give feedback (✓/✗, correct answer, explanation).",
        inputSchema: {
          type: "object",
          properties: {
            question: {
              type: "string",
              description: "The single quiz question to ask. Ask exactly one question per tool call.",
            },
            details: {
              type: "string",
              description: "Optional extra context or instructions shown under the question.",
            },
            options: {
              type: "array",
              items: {
                type: "object",
                properties: {
                  label: { type: "string", description: "Display label for the answer option." },
                  value: {
                    type: "string",
                    description: "Optional machine-readable value returned for the option. Defaults to label.",
                  },
                  description: {
                    type: "string",
                    description: "Optional extra detail shown below the option.",
                  },
                },
                required: ["label"],
              },
              minItems: 2,
              description: "The answer options (2 or more). Give each option a stable value string.",
            },
            multiSelect: {
              type: "boolean",
              description: "Set to true when more than one option is correct and the user must select all of them.",
            },
            correctAnswer: {
              description:
                "REQUIRED. The correct answer as option value(s). Single-select: string. Multi-select: array of strings.",
              anyOf: [{ type: "string" }, { type: "array", items: { type: "string" } }],
            },
            explanation: {
              type: "string",
              description:
                "REQUIRED. Explanation revealed AFTER the user answers (shown whether they got it right or wrong).",
            },
            shuffle: {
              type: "boolean",
              description:
                "Defaults to true: options are randomly reordered before display. Set to false only when option order is meaningful.",
            },
            selectedValues: {
              type: "array",
              items: { type: "string" },
              description: "Optional user selected option values when evaluating an answer.",
            },
            dontKnow: {
              type: "boolean",
              description: "Set to true if user selected 'I don't know'.",
            },
            userNote: {
              type: "string",
              description: "Optional user note or reasoning typed along with the answer.",
            },
          },
          required: ["question", "options", "correctAnswer", "explanation"],
        },
      },
      {
        name: "evaluate_quiz_response",
        description:
          "Grade a user selection against a quiz question spec, returning structured pass/fail results, correct answers, and explanation.",
        inputSchema: {
          type: "object",
          properties: {
            question: { type: "string" },
            options: {
              type: "array",
              items: {
                type: "object",
                properties: {
                  label: { type: "string" },
                  value: { type: "string" },
                },
                required: ["label"],
              },
            },
            correctAnswer: {
              anyOf: [{ type: "string" }, { type: "array", items: { type: "string" } }],
            },
            selectedValues: { type: "array", items: { type: "string" } },
            dontKnow: { type: "boolean" },
            explanation: { type: "string" },
          },
          required: ["question", "options", "correctAnswer", "explanation"],
        },
      },
    ];
  }

  private handleToolCall(id: any, name: string, args: any) {
    try {
      if (name === "quiz" || name === "evaluate_quiz_response") {
        const result = gradeQuiz({
          question: args.question,
          options: args.options as QuizOptionInput[],
          correctAnswer: args.correctAnswer,
          explanation: args.explanation,
          details: args.details,
          multiSelect: args.multiSelect,
          shuffle: args.shuffle,
          selectedValues: args.selectedValues,
          selectedIndices: args.selectedIndices,
          dontKnow: args.dontKnow,
          userNote: args.userNote,
        });

        this.sendResult(id, {
          content: [
            {
              type: "text",
              text: result.formattedOutput,
            },
          ],
          details: result,
        });
        return;
      }

      this.sendError(id, -32601, `Unknown tool: ${name}`);
    } catch (err) {
      this.sendResult(id, {
        content: [
          {
            type: "text",
            text: `Error executing ${name}: ${(err as Error).message}`,
          },
        ],
        isError: true,
      });
    }
  }

  private sendResult(id: any, result: any) {
    const response = { jsonrpc: "2.0", id, result };
    process.stdout.write(JSON.stringify(response) + "\n");
  }

  private sendError(id: any, code: number, message: string, data?: any) {
    const response = {
      jsonrpc: "2.0",
      id,
      error: { code, message, data },
    };
    process.stdout.write(JSON.stringify(response) + "\n");
  }
}
