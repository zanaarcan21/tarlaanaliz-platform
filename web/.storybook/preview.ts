// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import type { Preview } from '@storybook/react';

import '../src/app/globals.css';

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: '^on[A-Z].*' },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i
      }
    },
    backgrounds: {
      default: 'app-bg',
      values: [
        { name: 'app-bg', value: '#f8fafc' },
        { name: 'dark', value: '#0f172a' }
      ]
    },
    layout: 'centered'
  },
  globalTypes: {
    theme: {
      name: 'Theme',
      description: 'Global theme',
      defaultValue: 'light',
      toolbar: {
        icon: 'circlehollow',
        items: ['light', 'dark']
      }
    }
  },
  decorators: [
    (Story, context) => {
      const isDark = context.globals.theme === 'dark';
      return (
        <div className={isDark ? 'dark bg-slate-950 p-6 text-slate-100' : 'bg-slate-50 p-6 text-slate-900'}>
          <Story />
        </div>
      );
    }
  ]
};

export default preview;
