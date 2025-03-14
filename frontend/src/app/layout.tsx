import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Providers } from "./provides";


const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Creador de Ofertas Laborales - DarSalud",
  description: "Aplicación para automatizar la creación y publicación de ofertas laborales en Instagram",
  keywords: "trabajo, ofertas laborales, instagram, salud, médicos, empleos",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <Providers>
          <div className="max-w-screen-xl mx-auto">
            {children}
          </div>
        </Providers>
      </body>
    </html>
  );
}