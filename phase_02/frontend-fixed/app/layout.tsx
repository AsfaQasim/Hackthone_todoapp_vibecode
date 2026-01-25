import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Layout from '../components/Layout';
import MotionWrapper from '../components/MotionWrapper';
import ThreeDBackground from '../components/ThreeDBackground';

const inter = Inter({
  variable: "--font-inter",
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
        className={`${inter.variable} antialiased bg-gray-900 text-gray-100 relative overflow-x-hidden`}
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
