import { Geist } from 'next/font/google';
import localFont from 'next/font/local';
import { ThemeProvider } from '@/components/app/theme-provider';
import { ThemeToggle } from '@/components/app/theme-toggle';
import { cn } from '@/lib/shadcn/utils';
import '@/styles/globals.css';

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
});

const commitMono = localFont({
  display: 'swap',
  variable: '--font-commit-mono',
  src: [
    {
      path: '../fonts/CommitMono-400-Regular.otf',
      weight: '400',
      style: 'normal',
    },
    {
      path: '../fonts/CommitMono-700-Regular.otf',
      weight: '700',
      style: 'normal',
    },
    {
      path: '../fonts/CommitMono-400-Italic.otf',
      weight: '400',
      style: 'italic',
    },
    {
      path: '../fonts/CommitMono-700-Italic.otf',
      weight: '700',
      style: 'italic',
    },
  ],
});

interface RootLayoutProps {
  children: React.ReactNode;
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html
      lang="es"
      suppressHydrationWarning
      className={cn(geistSans.variable, commitMono.variable, 'scroll-smooth font-sans antialiased')}
    >
      <head>
        <title>¿Bueno, me escuchas? · Hokusei Digital</title>
        <meta
          name="description"
          content="Agente de voz de Mexico Tech Week 2026, hecho con LiveKit por Hokusei Digital"
        />
      </head>
      <body className="overflow-x-hidden">
        <ThemeProvider attribute="class" defaultTheme="dark" enableSystem disableTransitionOnChange>
          <header className="fixed top-0 left-0 z-50 hidden w-full flex-row justify-between p-6 md:flex">
            <a
              target="_blank"
              rel="noopener noreferrer"
              href="https://hokuseidigital.com"
              className="flex scale-100 items-center gap-3 transition-transform duration-300 hover:scale-105"
            >
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src="/hokusei-logo.svg" alt="Hokusei Digital" className="size-9" />
              <span className="text-foreground font-mono text-xs font-bold tracking-wider uppercase">
                Hokusei Digital
              </span>
            </a>
            <span className="text-foreground font-mono text-xs font-bold tracking-wider uppercase">
              Hecho con{' '}
              <a
                target="_blank"
                rel="noopener noreferrer"
                href="https://docs.livekit.io/agents"
                className="underline underline-offset-4"
              >
                LiveKit Agents
              </a>
            </span>
          </header>

          {children}
          <div className="group fixed bottom-0 left-1/2 z-50 mb-2 -translate-x-1/2">
            <ThemeToggle className="translate-y-20 transition-transform delay-150 duration-300 group-hover:translate-y-0" />
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
