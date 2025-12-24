'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function LoginPage() {
  const [emailOrTc, setEmailOrTc] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  // GERÇEK GİRİŞ (Backend ile)
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
        const response = await fetch("http://localhost:8000/api/v1/auth/token", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
                username: emailOrTc,
                password: password,
            }),
        });

        const data = await response.json();

        if (response.ok && data.access_token) {
            localStorage.setItem('token', data.access_token);
            router.push('/chat');
        } else {
            setError(data.detail || "Giriş başarısız");
        }

    } catch (error) {
      console.error('Login error:', error);
      setError('Sunucuya bağlanılamadı');
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="flex min-h-screen bg-white dark:bg-[#0f172a] transition-colors duration-500">
      
     
      {/* SOL PANEL (Gradient) */}
      <div className="hidden lg:flex w-1/2 items-center justify-center p-8 
        bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 
        dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 
        transition-all duration-500 relative overflow-hidden">
        
        <div className="absolute top-0 left-0 w-full h-full bg-white/10 backdrop-blur-sm dark:bg-black/20"></div>
        
        <div className="text-center relative z-10">
          <div className="mb-8 flex justify-center">
            <div className="w-24 h-24 rounded-3xl flex items-center justify-center text-white font-bold text-4xl shadow-2xl 
              bg-white/20 backdrop-blur-md border border-white/30
              dark:bg-slate-800/50 dark:border-slate-700 transition-all duration-500">
              AI
            </div>
          </div>
          <h1 className="text-white text-5xl font-bold mb-6 drop-shadow-lg">
            AI Çizim Asistanı
          </h1>
          <p className="text-white/90 text-xl font-light tracking-wide">
            Yapay zeka ile hayal gücünü sanata dönüştür.
          </p>
        </div>
      </div>

      {/* SAĞ PANEL (Giriş Formu) */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
        <div className="w-full max-w-md p-10 rounded-3xl shadow-2xl 
          bg-white dark:bg-[#1e293b] 
          border border-gray-100 dark:border-slate-700
          transition-all duration-500">
          
          <div className="text-center mb-10">
            <h2 className="text-3xl font-bold mb-2 text-gray-800 dark:text-white transition-colors duration-300">
              Hoş Geldiniz 
            </h2>
            <p className="text-gray-500 dark:text-gray-400 transition-colors duration-300">
              Devam etmek için giriş yapın
            </p>
          </div>

          <form onSubmit={handleLogin} className="space-y-6">
            {/* Inputlar */}
            <div>
              <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300 transition-colors duration-300">
                Email veya TC Kimlik No
              </label>
              <input
                type="text"
                className="w-full px-4 py-3 rounded-xl border outline-none transition-all duration-300
                  bg-gray-50 border-gray-200 text-gray-900 focus:ring-2 focus:ring-indigo-500 focus:border-transparent
                  dark:bg-[#334155] dark:border-slate-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-400"
                placeholder="ornek@email.com"
                value={emailOrTc}
                onChange={(e) => setEmailOrTc(e.target.value)}
                disabled={loading}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300 transition-colors duration-300">
                Şifre
              </label>
              <input
                type="password"
                className="w-full px-4 py-3 rounded-xl border outline-none transition-all duration-300
                  bg-gray-50 border-gray-200 text-gray-900 focus:ring-2 focus:ring-indigo-500 focus:border-transparent
                  dark:bg-[#334155] dark:border-slate-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-400"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={loading}
              />
            </div>

            {error && (
              <div className="p-4 rounded-xl text-sm font-medium 
                bg-red-50 text-red-600 border border-red-100
                dark:bg-red-900/20 dark:text-red-300 dark:border-red-800 transition-colors duration-300">
                ⚠️ {error}
              </div>
            )}

            {/* Gerçek Giriş Butonu */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-4 px-6 rounded-xl font-bold text-white shadow-lg transform transition-all duration-300
                bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 hover:scale-[1.02] active:scale-95
                dark:from-indigo-500 dark:to-purple-500 disabled:opacity-70 disabled:cursor-not-allowed"
            >
              {loading ? 'Giriş Yapılıyor...' : 'Giriş Yap'}
            </button>


          </form>

          <div className="mt-8 flex items-center justify-between text-sm">
            <Link
              href="/forgot-password"
              className="font-medium text-gray-500 hover:text-indigo-600 dark:text-gray-400 dark:hover:text-indigo-400 transition-colors duration-300"
            >
              Şifremi unuttum?
            </Link>
            
            <Link
              href="/signup" 
              className="font-bold text-indigo-600 hover:text-indigo-800 dark:text-indigo-400 dark:hover:text-indigo-300 transition-colors duration-300"
            >
              Hesap oluştur
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}