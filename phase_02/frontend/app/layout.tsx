import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Layout from '../components/Layout';
import MotionWrapper from '../components/MotionWrapper';
import ThreeDBackground from '../components/ThreeDBackground';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "VibeCode - Premium Task Management",
  description: "Professional task management solution with stunning UI",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-gray-900 text-gray-100 relative overflow-hidden`}
      >
        <ThreeDBackground />
        <MotionWrapper>
          <Layout>
            {children}
          </Layout>
        </MotionWrapper>
      </body>
    </html>
  );
}
