export async function copyCommand(text, { write, select, announce }) {
  if (write) {
    try {
      await write(text);
      announce("Commands copied.");
      return "copied";
    } catch {
      // Clipboard permission can be denied even when the API exists.
    }
  }

  select(text);
  announce("Commands selected. Press Ctrl+C to copy.");
  return "selected";
}

function selectNode(node) {
  const selection = window.getSelection();
  const range = document.createRange();
  range.selectNodeContents(node);
  selection.removeAllRanges();
  selection.addRange(range);
}

function bindCopyControl() {
  const button = document.querySelector("[data-copy-command]");
  const command = document.querySelector("#quick-start-command");
  const status = document.querySelector("#copy-status");

  if (!button || !command || !status) {
    return;
  }

  button.addEventListener("click", () => {
    const write = navigator.clipboard?.writeText
      ? navigator.clipboard.writeText.bind(navigator.clipboard)
      : undefined;

    void copyCommand(command.textContent.trim(), {
      write,
      select: () => selectNode(command),
      announce: (message) => {
        status.textContent = message;
      },
    });
  });
}

if (typeof document !== "undefined") {
  bindCopyControl();
}
