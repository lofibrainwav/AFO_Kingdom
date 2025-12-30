# Neovim Ruff + Pyright Guide (2025)

This guide describes how to achieve a "Chancellor-level" development experience in Neovim using Ruff and Pyright.

## 📦 Required Plugins

Using `lazy.nvim`, ensure you have these components:

```lua
return {
  -- LSP Configuration
  {
    "neovim/nvim-lspconfig",
    dependencies = {
      "williamboman/mason.nvim",
      "williamboman/mason-lspconfig.nvim",
    },
    config = function()
      local lspconfig = require("lspconfig")
      
      -- Ruff LSP (Fast Linting & Formatting)
      lspconfig.ruff_lsp.setup({
        on_attach = function(client, bufnr)
          -- Disable hover in favor of Pyright
          client.server_capabilities.hoverProvider = false
        end,
      })

      -- Pyright (Advanced Type Checking)
      lspconfig.pyright.setup({
        settings = {
          python = {
            analysis = {
              typeCheckingMode = "standard", -- basic, standard, or strict
              autoSearchPaths = true,
              useLibraryCodeForTypes = true,
            },
          },
        },
      })
    end,
  },

  -- Formatting (Modern Alternative to null-ls)
  {
    "stevearc/conform.nvim",
    opts = {
      formatters_by_ft = {
        python = { "ruff_format", "ruff_fix", "ruff_organize_imports" },
      },
      format_on_save = {
        timeout_ms = 500,
        lsp_fallback = true,
      },
    },
  },
}
```

## ⚖️ Philosophical Balance (眞·美)

1. **眞 (Truth)**: Pyright provides real-time type verification. Use `:LspLog` if you suspect the server isn't picking up your venv.
2. **美 (Beauty)**: Ruff ensures your code is formatted and lint-free. `conform.nvim` handles this automatically on save.
3. **孝 (Filial Piety)**: `mason.nvim` manages the installation of `ruff-lsp` and `pyright` for you, reducing manual friction.

## 🛠️ Diagnostics & Commands

- `]d` / `[d`: Jump to next/previous diagnostic (Ruff or Pyright).
- `<leader>ca`: Code actions (use this to apply Ruff fixes).
- `:LspInfo`: Verify that both `ruff_lsp` and `pyright` are attached to the buffer.
