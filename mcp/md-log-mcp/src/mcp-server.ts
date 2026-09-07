import * as readline from "node:readline";
import { MdLogger } from "./logger.js";

export class McpServer {
  private logger: MdLogger;

  constructor() {
    this.logger = new MdLogger();
  }

  public start() {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
      terminal: false,
    });

    rl.on("line", async (line: string) => {
      const trimmed = line.trim();
      if (!trimmed) return;

      try {
        const message = JSON.parse(trimmed);
        await this.handleMessage(message);
      } catch (err) {
        this.sendError(null, -32700, "Parse error", String(err));
      }
    });

    process.stderr.write("md-log MCP Server started on stdio\n");
  }

  private async handleMessage(msg: any) {
    if (!msg || typeof msg !== "object") return;

    // Handle notifications (no id)
    if (msg.id === undefined || msg.id === null) {
      if (msg.method === "notifications/initialized") {
        // Acknowledge initialization notification
      }
      return;
    }

    const { id, method, params } = msg;

    switch (method) {
      case "initialize":
        this.sendResult(id, {
          protocolVersion: "2024-11-05",
          capabilities: {
            tools: {},
          },
          serverInfo: {
            name: "md-log-mcp",
            version: "1.0.0",
          },
        });
        break;

      case "tools/list":
        this.sendResult(id, {
          tools: this.getToolDefinitions(),
        });
        break;

      case "tools/call":
        await this.handleToolCall(id, params?.name, params?.arguments || {});
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
        name: "set_log_file",
        description: "Set the active Markdown file path to mirror session logs and callouts to.",
        inputSchema: {
          type: "object",
          properties: {
            filepath: { type: "string", description: "Path to the markdown file" },
            create_if_missing: {
              type: "boolean",
              description: "Create the file if it does not exist (default: true)",
              default: true,
            },
          },
          required: ["filepath"],
        },
      },
      {
        name: "stop_logging",
        description: "Stop mirroring session logs to the active markdown file.",
        inputSchema: { type: "object", properties: {} },
      },
      {
        name: "get_log_status",
        description: "Get current status and active markdown log file path.",
        inputSchema: { type: "object", properties: {} },
      },
      {
        name: "log_user_message",
        description: "Append a user prompt callout (> [!quote] YOU) to the markdown log.",
        inputSchema: {
          type: "object",
          properties: {
            text: { type: "string", description: "The user prompt text to log" },
          },
          required: ["text"],
        },
      },
      {
        name: "log_assistant_message",
        description: "Append an assistant response callout (> [!abstract]) to the markdown log.",
        inputSchema: {
          type: "object",
          properties: {
            text: { type: "string", description: "The assistant text to log" },
            sender_name: {
              type: "string",
              description: "Sender label (default: ASSISTANT)",
              default: "ASSISTANT",
            },
          },
          required: ["text"],
        },
      },
      {
        name: "log_question",
        description: "Append a question or quiz callout (> [!question]) to the markdown log.",
        inputSchema: {
          type: "object",
          properties: {
            question: { type: "string", description: "Question text" },
            options: {
              type: "array",
              items: { type: "string" },
              description: "Optional list of choice options",
            },
            context: { type: "string", description: "Optional background details or context" },
            label: {
              type: "string",
              description: "Callout title label (default: Question)",
              default: "Question",
            },
          },
          required: ["question"],
        },
      },
      {
        name: "log_quiz_answer",
        description: "Append quiz feedback callout (> [!success] / > [!failure]) to the markdown log.",
        inputSchema: {
          type: "object",
          properties: {
            status: { type: "string", description: "Optional status ('cancelled', 'unavailable')" },
            dont_know: { type: "boolean", description: "True if user selected 'I don't know'" },
            correct: { type: "boolean", description: "True if user answer was correct" },
            answers: {
              type: "array",
              items: {
                type: "object",
                properties: {
                  index: { type: "number" },
                  label: { type: "string" },
                },
              },
            },
            correct_indices: { type: "array", items: { type: "number" } },
            note: { type: "string" },
            explanation: { type: "string" },
          },
        },
      },
      {
        name: "log_ask_answer",
        description: "Append user answer callout (> [!example] Answer) for a question tool call.",
        inputSchema: {
          type: "object",
          properties: {
            status: { type: "string" },
            answers: {
              type: "array",
              items: {
                type: "object",
                properties: {
                  label: { type: "string" },
                  type: { type: "string" },
                },
              },
            },
          },
        },
      },
      {
        name: "log_custom_entry",
        description: "Append a custom text or markdown callout (> [!note], > [!tip], > [!warning], etc.) to the log file.",
        inputSchema: {
          type: "object",
          properties: {
            text: { type: "string", description: "Text body to log" },
            callout_type: {
              type: "string",
              description: "Callout type (note, tip, warning, quote, example, abstract, etc.)",
            },
            title: { type: "string", description: "Callout title text" },
          },
          required: ["text"],
        },
      },
    ];
  }

  private async handleToolCall(id: any, toolName: string, args: any) {
    try {
      let resultText = "";

      switch (toolName) {
        case "set_log_file": {
          const filepath = args.filepath;
          const createIfMissing = args.create_if_missing !== false;
          const resolved = this.logger.setLogFile(filepath, createIfMissing);
          resultText = `Log file set to: ${resolved}`;
          break;
        }

        case "stop_logging": {
          const prev = this.logger.stopLogging();
          resultText = prev ? `Stopped logging to: ${prev}` : "No active log file was set.";
          break;
        }

        case "get_log_status": {
          const activeFile = this.logger.getLogFile();
          resultText = activeFile
            ? `Logging is ACTIVE -> ${activeFile}`
            : "Logging is INACTIVE (no file linked).";
          break;
        }

        case "log_user_message": {
          const ok = await this.logger.logUserMessage(args.text || "");
          resultText = ok
            ? "User message logged successfully."
            : "Failed to log user message (no active log file or empty message).";
          break;
        }

        case "log_assistant_message": {
          const ok = await this.logger.logAssistantMessage(
            args.text || "",
            args.sender_name || "ASSISTANT"
          );
          resultText = ok
            ? "Assistant message logged successfully."
            : "Failed to log assistant message (no active log file or empty message).";
          break;
        }

        case "log_question": {
          const rawOptions: any[] = Array.isArray(args.options) ? args.options : [];
          const options = rawOptions.map((o) =>
            typeof o === "string" ? { label: o } : { label: String(o?.label || o) }
          );
          const ok = await this.logger.logQuestion(
            args.question || "",
            options,
            args.context,
            args.label || "Question"
          );
          resultText = ok
            ? "Question logged successfully."
            : "Failed to log question (no active log file).";
          break;
        }

        case "log_quiz_answer": {
          const ok = await this.logger.logQuizAnswer({
            status: args.status,
            dontKnow: args.dont_know,
            correct: args.correct,
            answers: args.answers,
            correctIndices: args.correct_indices,
            note: args.note,
            explanation: args.explanation,
          });
          resultText = ok
            ? "Quiz answer logged successfully."
            : "Failed to log quiz answer (no active log file).";
          break;
        }

        case "log_ask_answer": {
          const ok = await this.logger.logAskAnswer({
            status: args.status,
            answers: args.answers,
          });
          resultText = ok
            ? "Ask answer logged successfully."
            : "Failed to log ask answer (no active log file).";
          break;
        }

        case "log_custom_entry": {
          const ok = await this.logger.logCustomEntry(
            args.text || "",
            args.callout_type,
            args.title
          );
          resultText = ok
            ? "Custom entry logged successfully."
            : "Failed to log entry (no active log file).";
          break;
        }

        default:
          this.sendError(id, -32601, `Unknown tool: ${toolName}`);
          return;
      }

      this.sendResult(id, {
        content: [
          {
            type: "text",
            text: resultText,
          },
        ],
      });
    } catch (err) {
      this.sendResult(id, {
        content: [
          {
            type: "text",
            text: `Error executing tool ${toolName}: ${String(err)}`,
          },
        ],
        isError: true,
      });
    }
  }

  private sendResult(id: any, result: any) {
    const response = {
      jsonrpc: "2.0",
      id,
      result,
    };
    process.stdout.write(JSON.stringify(response) + "\n");
  }

  private sendError(id: any, code: number, message: string, data?: any) {
    const response = {
      jsonrpc: "2.0",
      id,
      error: {
        code,
        message,
        data,
      },
    };
    process.stdout.write(JSON.stringify(response) + "\n");
  }
}
