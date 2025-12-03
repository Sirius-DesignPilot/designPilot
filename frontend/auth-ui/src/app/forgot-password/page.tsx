'use client';

import Link from 'next/link';

export default function ForgotPasswordPage() {
  return (
    <div className="flex min-h-screen bg-white dark:bg-[#1a1f3a] transition-colors duration-300">
      
      {/* SOL PANEL */}
      <div className="hidden lg:flex w-1/2 items-center justify-center p-8 bg-gradient-to-br from-blue-400 to-indigo-500 dark:from-[#2d3454] dark:to-[#1e2440] transition-all duration-300 relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-full bg-white/10 backdrop-blur-sm dark:bg-black/20"></div>
        <div className="text-center relative z-10">
          <div className="mb-8 flex justify-center">
            <div className="w-24 h-24 rounded-3xl flex items-center justify-center text-white font-bold text-4xl shadow-2xl bg-white/20 backdrop-blur-md border border-white/30 dark:bg-slate-800/50 dark:border-slate-700">
              ?
            </div>
          </div>
          <h1 className="text-white text-5xl font-bold mb-6 drop-shadow-lg">Şifreni mi Unuttun?</h1>
          <p className="text-white/90 text-xl font-light">Merak etme, hesabını kurtarmak çok kolay.</p>
        </div>
      </div>

      {/* SAĞ PANEL */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
        <div className="w-full max-w-md p-10 rounded-3xl shadow-2xl bg-white dark:bg-[#1e293b] border border-gray-100 dark:border-slate-700 transition-all duration-300">
          <h2 className="text-2xl font-bold text-center text-gray-800 dark:text-white mb-4">Şifre Sıfırlama</h2>
          <p className="text-sm text-gray-600 dark:text-gray-400 text-center mb-8">
            Hesabınıza kayıtlı e-posta adresinizi girin. Size sıfırlama bağlantısı göndereceğiz.
          </p>
          
          <form className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">Email Adresi</label>
              <input 
                type="email" 
                placeholder="ornek@email.com" 
                className="w-full px-4 py-3 rounded-xl border outline-none transition-all duration-300 bg-gray-50 border-gray-200 text-gray-900 focus:ring-2 focus:ring-blue-500 dark:bg-[#334155] dark:border-slate-600 dark:text-white dark:focus:ring-indigo-400"
              />
            </div>

            <button className="w-full py-4 px-6 rounded-xl font-bold text-white shadow-lg bg-blue-600 hover:bg-blue-700 dark:bg-indigo-600 dark:hover:bg-indigo-500 transition-all duration-300">
              Bağlantı Gönder
            </button>

            <div className="text-center mt-4">
              <Link href="/login" className="text-sm text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-indigo-400 flex items-center justify-center gap-1 transition-colors">
                <span>←</span> Giriş ekranına dön
              </Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}