'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function SignupPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (password !== passwordConfirm) {
      setError('Şifreler eşleşmiyor!');
      return;
    }

    setLoading(true);

    try {
      // Backend isteği
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        // Kayıt başarılıysa giriş sayfasına yönlendir
        router.push('/login');
      } else {
        setError(data.message || 'Kayıt başarısız');
      }
    } catch (error) {
      console.error('Signup error:', error);
      setError('Sunucuya bağlanılamadı');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-white dark:bg-[#0f172a] transition-colors duration-500">
      
      {/* SOL PANEL (Gradient) */}
      <div className="hidden lg:flex w-1/2 items-center justify-center p-8 
        bg-gradient-to-br from-[#FF6584] to-[#6C63FF] 
        dark:from-[#1e2440] dark:to-[#2d3454] 
        transition-all duration-500 relative overflow-hidden">
        
        <div className="absolute top-0 left-0 w-full h-full bg-white/10 backdrop-blur-sm dark:bg-black/20"></div>
        
        <div className="text-center relative z-10">
          <div className="mb-8 flex justify-center">
            <div className="w-24 h-24 rounded-3xl flex items-center justify-center text-white font-bold text-4xl shadow-2xl 
              bg-gradient-to-br from-orange-500 to-pink-500 
              dark:from-blue-600 dark:to-indigo-600 
              transition-colors duration-300">
              AI
            </div>
          </div>
          <h1 className="text-white text-5xl font-bold mb-6 drop-shadow-lg">
            Aramıza Katılın
          </h1>
          <p className="text-white/90 text-xl font-light tracking-wide">
            Yaratıcılığınızı keşfetmek için hemen bir hesap oluşturun.
          </p>
        </div>
      </div>

      {/* SAĞ PANEL (Form) */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
        <div className="w-full max-w-md p-10 rounded-3xl shadow-2xl 
          bg-white dark:bg-[#1e293b] 
          border border-gray-100 dark:border-slate-700
          transition-all duration-500">
          
          <h2 className="text-3xl font-bold mb-6 text-center text-gray-800 dark:text-white transition-colors duration-300">
            Hesap Oluştur
          </h2>

          <form onSubmit={handleSignup} className="space-y-5">
            {/* Email */}
            <div>
              <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">Email Adresi</label>
              <input
                type="email"
                className="w-full px-4 py-3 rounded-xl border outline-none transition-all duration-300 bg-gray-50 border-gray-200 text-gray-900 focus:ring-2 focus:ring-[#FF6584] dark:bg-[#334155] dark:border-slate-600 dark:text-white dark:focus:ring-indigo-400"
                placeholder="ornek@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={loading}
              />
            </div>

            {/* Şifre */}
            <div>
              <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">Şifre</label>
              <input
                type="password"
                className="w-full px-4 py-3 rounded-xl border outline-none transition-all duration-300 bg-gray-50 border-gray-200 text-gray-900 focus:ring-2 focus:ring-[#FF6584] dark:bg-[#334155] dark:border-slate-600 dark:text-white dark:focus:ring-indigo-400"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={loading}
              />
            </div>

            {/* Şifre Tekrar */}
            <div>
              <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">Şifre Tekrar</label>
              <input
                type="password"
                className="w-full px-4 py-3 rounded-xl border outline-none transition-all duration-300 bg-gray-50 border-gray-200 text-gray-900 focus:ring-2 focus:ring-[#FF6584] dark:bg-[#334155] dark:border-slate-600 dark:text-white dark:focus:ring-indigo-400"
                placeholder="••••••••"
                value={passwordConfirm}
                onChange={(e) => setPasswordConfirm(e.target.value)}
                required
                disabled={loading}
              />
            </div>

            {error && (
              <div className="p-4 rounded-xl text-sm font-medium bg-red-50 text-red-600 border border-red-100 dark:bg-red-900/20 dark:text-red-300 dark:border-red-800">
                ⚠️ {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-4 px-6 rounded-xl font-bold text-white shadow-lg transform transition-all duration-300 bg-gradient-to-r from-[#FF6584] to-[#e65a77] hover:scale-[1.02] dark:from-indigo-600 dark:to-purple-600 disabled:opacity-70 disabled:cursor-not-allowed"
            >
              {loading ? 'Kaydediliyor...' : 'Kayıt Ol'}
            </button>
          </form>

          <div className="mt-8 text-center text-sm">
            <span className="text-gray-600 dark:text-gray-400">Zaten hesabın var mı? </span>
            <Link href="/login" className="font-bold text-[#FF6584] hover:text-[#e65a77] dark:text-indigo-400 dark:hover:text-indigo-300 transition-colors">
              Giriş Yap
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}