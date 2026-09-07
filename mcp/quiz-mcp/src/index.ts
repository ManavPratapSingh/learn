#!/usr/bin/env node
import { QuizMcpServer } from "./mcp-server.js";

const server = new QuizMcpServer();
server.start();
