declare module 'vue' {
  import { DefineComponent } from '@vue/runtime-core'
  import { createApp } from '@vue/runtime-dom'
  const component: DefineComponent<{}, {}, any>
  export default component
  export * from '@vue/runtime-core'
  export { createApp }
} 