/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */

import js from "@eslint/js";

export default [
  {
    ignores: [".next/**", "dist/**", "coverage/**", "**/*.{ts,tsx}"],
  },
  js.configs.recommended,
  {
    files: ["**/*.{js,mjs,cjs}"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        caches: "readonly",
        console: "readonly",
        fetch: "readonly",
        process: "readonly",
        self: "readonly",
      },
    },
    rules: {
      "no-console": ["warn", { allow: ["warn", "error", "info"] }],
    },
  },
];
