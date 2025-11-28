export interface AppConfig {
  pageTitle: string;
  pageDescription: string;
  companyName: string;

  supportsChatInput: boolean;
  supportsVideoInput: boolean;
  supportsScreenShare: boolean;
  isPreConnectBufferEnabled: boolean;

  logo: string;
  startButtonText: string;
  accent?: string;
  logoDark?: string;
  accentDark?: string;

  // for LiveKit Cloud Sandbox
  sandboxId?: string;
  agentName?: string;
}

export const APP_CONFIG_DEFAULTS: AppConfig = {
  companyName: 'Burger King',
  pageTitle: 'Burger King Voice Order',
  pageDescription:
    'Order flame-grilled burgers with your voice. Have it your way.',

  supportsChatInput: true,
  supportsVideoInput: false,
  supportsScreenShare: false,
  isPreConnectBufferEnabled: true,

  logo: '/logo.svg', // We'll keep the file but ignore it visually if we use text/emoji
  accent: '#D62300', // Burger King Red
  logoDark: '/logo.svg',
  accentDark: '#E55F25', // Burger King Orange
  startButtonText: 'Start Ordering',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: 'freshmarket-agent',
};
