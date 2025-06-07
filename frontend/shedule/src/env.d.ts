/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_TITLE: string
  // більше змінних середовища...
}

interface ImportMeta {
  readonly env: ImportMetaEnv
} 