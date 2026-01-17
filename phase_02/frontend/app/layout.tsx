import './globals.css';
// layout.tsx
import AuthProvider from "../components/AuthProvider"; // ✅

import Header from '../components/Header';

export const metadata = {
  title: 'Todo App',
  description: 'A secure todo application with user authentication',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">
        <AuthProvider>
          <div className="flex flex-col min-h-screen">
            <Header />
            <main className="flex-grow">{children}</main>

            <footer className="bg-white border-t mt-8 py-6">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-gray-500">
                © {new Date().getFullYear()} Todo App. All rights reserved.
              </div>
            </footer>
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}
