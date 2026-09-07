import * as readline from "node:readline";
import { processQuestion, AskOptionInput } from "./ask-engine.js";

export class AskUserQuestionMcpServer {
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

    process.stderr.write("ask_user_question MCP Server started on stdio\n");
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
          serverInfo: { name: "ask-user-question-mcp", version: "1.0.0" },
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
        name: "ask_user_question",
        description:
          "Ask the user a single question and pause execution until they answer. Use this when requirements are ambiguous, user preferences are needed, or a decision affects implementation.",
        inputSchema: {
          type: "object",
          properties: {
            question: {
              type: "string",
              description: "The single question to ask the user. Ask exactly one question per tool call.",
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
                  label: {
                    type: "string",
                    description: 'Display label. Recommending an option? Place first & append "(Recommended)".',
                  },
                  value: {
                    type: "string",
                    description: "Optional machine-readable value returned for option. Defaults to label.",
                  },
                  description: {
                    type: "string",
                    description: "Optional extra detail shown below the option.",
                  },
                },
                required: ["label"],
              },
              description:
                "Optional multiple-choice options. Omit or pass empty for free-form text input. Users can always select Other.",
            },
            multiSelect: {
              type: "boolean",
              description: "Set to true to allow multiple answers to be selected for a question.",
            },
            selectedAnswers: {
              type: "array",
              items: {
                type: "object",
                properties: {
                  index: { type: "number" },
                  value: { type: "string" },
                  text: { type: "string" },
                  type: { type: "string" },
                },
              },
              description: "Optional user responses when evaluating or recording answers.",
            },
            otherText: {
              type: "string",
              description: "Optional custom write-in text typed when selecting 'Other'.",
            },
            textResponse: {
              type: "string",
              description: "Optional free-form text response.",
            },
          },
          required: ["question"],
        },
      },
      {
        name: "process_question_answer",
        description: "Process and format user answers for an ask_user_question call.",
        inputSchema: {
          type: "object",
          properties: {
            question: { type: "string" },
            options: { type: "array", items: { type: "object" } },
            selectedAnswers: { type: "array", items: { type: "object" } },
            otherText: { type: "string" },
            textResponse: { type: "string" },
          },
          required: ["question"],
        },
      },
    ];
  }

  private handleToolCall(id: any, name: string, args: any) {
    try {
      if (name === "ask_user_question" || name === "process_question_answer") {
        const result = processQuestion({
          question: args.question,
          details: args.details,
          options: args.options as AskOptionInput[],
          multiSelect: args.multiSelect,
          selectedAnswers: args.selectedAnswers,
          otherText: args.otherText,
          textResponse: args.textResponse,
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
