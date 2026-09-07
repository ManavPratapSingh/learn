#!/usr/bin/env node
import { AskUserQuestionMcpServer } from "./mcp-server.js";

const server = new AskUserQuestionMcpServer();
server.start();
