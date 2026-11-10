(function () {
  var PROMPT_TEXT =
    "获取 https://ai-works-workshop.app.workbuddy.host/setup/install.md?sharecode=GVVF43H4ID 中的训练营技能安装说明，按照说明下载并校验四个技能包，确认 WorkBuddy 技能目录后新增安装；遇到同名冲突停止，不覆盖已有文件。";

  function clearManual(anchor) {
    var existing = anchor.parentNode.querySelector(".manual-copy");
    if (existing) existing.remove();
  }

  function showManual(anchor, text, label) {
    clearManual(anchor);
    var input = document.createElement("textarea");
    input.className = "manual-copy";
    input.readOnly = true;
    input.value = text;
    input.setAttribute("aria-label", label);
    anchor.insertAdjacentElement("afterend", input);
    input.focus();
    input.select();
  }

  function legacyCopy(text) {
    var input = document.createElement("textarea");
    input.value = text;
    input.setAttribute("readonly", "");
    input.style.position = "fixed";
    input.style.top = "0";
    input.style.left = "0";
    input.style.width = "1px";
    input.style.height = "1px";
    input.style.opacity = "0";
    document.body.appendChild(input);
    input.focus();
    input.select();
    var ok = false;
    try {
      ok = document.execCommand("copy");
    } catch (error) {
      ok = false;
    }
    input.remove();
    return ok;
  }

  function copyText(text, onCopied, onFailed) {
    var canUseClipboard =
      window.isSecureContext &&
      navigator.clipboard &&
      typeof navigator.clipboard.writeText === "function";

    if (canUseClipboard) {
      navigator.clipboard.writeText(text).then(onCopied).catch(function () {
        if (legacyCopy(text)) onCopied();
        else onFailed();
      });
      return;
    }

    if (legacyCopy(text)) onCopied();
    else onFailed();
  }

  function wirePromptButton() {
    var button = document.getElementById("copy-button");
    var label = document.getElementById("copy-button-label");
    var status = document.getElementById("copy-status");
    if (!button || !label || !status) return;

    var resetTimer = null;

    button.addEventListener("click", function () {
      copyText(
        PROMPT_TEXT,
        function () {
          label.textContent = "已复制";
          status.textContent = "";
          clearManual(status);
          if (resetTimer) window.clearTimeout(resetTimer);
          resetTimer = window.setTimeout(function () {
            label.textContent = "点击复制";
          }, 1600);
        },
        function () {
          label.textContent = "点击复制";
          if (resetTimer) window.clearTimeout(resetTimer);
          status.textContent = "浏览器没有完成复制。请选中下方文字，手动复制。";
          showManual(status, PROMPT_TEXT, "手动复制安装提示词");
        }
      );
    });
  }

  function wireCaseButton(block) {
    var button = block.querySelector(".case-copy");
    var text = block.querySelector(".case-text");
    if (!button || !text) return;

    var resetTimer = null;

    button.addEventListener("click", function () {
      var value = (text.textContent || "").replace(/^\s+|\s+$/g, "");
      copyText(
        value,
        function () {
          button.textContent = "已复制";
          clearManual(block);
          if (resetTimer) window.clearTimeout(resetTimer);
          resetTimer = window.setTimeout(function () {
            button.textContent = "复制";
          }, 1600);
        },
        function () {
          button.textContent = "复制";
          if (resetTimer) window.clearTimeout(resetTimer);
          showManual(block, value, "手动复制课程案例");
        }
      );
    });
  }

  wirePromptButton();

  var caseBlocks = document.querySelectorAll(".case-block");
  for (var i = 0; i < caseBlocks.length; i++) {
    wireCaseButton(caseBlocks[i]);
  }
})();
