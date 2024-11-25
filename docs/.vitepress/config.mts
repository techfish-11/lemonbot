import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "LemonBot",
  description: "国産多機能Bot",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: '導入する', link: 'https://discord.com/oauth2/authorize?client_id=1310198598213963858' }
    ],

    sidebar: [
      {
        text: 'Docs',
        items: [
          { text: 'LemonBotとは', link: '/lemon/index.md' },
          { text: 'コマンド使用方法', link: '/lemon/command-use.md' },
          { text: 'botサポート', link: '/lemon/support.md' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/techfish-11/lemonbot' }
    ]
  }
})
