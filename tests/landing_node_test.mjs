import assert from "node:assert/strict";
import test from "node:test";

// Named *_node_test.mjs so Vitest does not collect this Node standard-library suite.

import { copyCommand } from "../landing.mjs";


const command = "scripts/install.sh";

test("copyCommand writes to the clipboard and announces success", async () => {
  const calls = [];

  const result = await copyCommand(command, {
    write: async (text) => calls.push(["write", text]),
    select: () => calls.push(["select"]),
    announce: (message) => calls.push(["announce", message]),
  });

  assert.equal(result, "copied");
  assert.deepEqual(calls, [
    ["write", command],
    ["announce", "Commands copied."],
  ]);
});

test("copyCommand selects the command when clipboard writing is unavailable", async () => {
  const calls = [];

  const result = await copyCommand(command, {
    select: (text) => calls.push(["select", text]),
    announce: (message) => calls.push(["announce", message]),
  });

  assert.equal(result, "selected");
  assert.deepEqual(calls, [
    ["select", command],
    ["announce", "Commands selected. Press Ctrl+C to copy."],
  ]);
});

test("copyCommand falls back when the clipboard rejects the write", async () => {
  const calls = [];

  const result = await copyCommand(command, {
    write: async () => {
      throw new Error("permission denied");
    },
    select: (text) => calls.push(["select", text]),
    announce: (message) => calls.push(["announce", message]),
  });

  assert.equal(result, "selected");
  assert.deepEqual(calls, [
    ["select", command],
    ["announce", "Commands selected. Press Ctrl+C to copy."],
  ]);
});
