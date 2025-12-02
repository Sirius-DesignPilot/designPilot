import Link from 'next/link';

export default function LoginPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-100 p-6">
      <div className="w-full max-w-md bg-white rounded-lg shadow-lg shadow-gray-700 p-8 text-black">
        <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">Giriş Yap</h2>
        
        <form className="space-y-4">
          {/* Email Kutucuğu */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email Adresi</label>
            <input 
              type="email" 
              placeholder="ornek@email.com" 
              className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
            />
          </div>

          {/* Şifre Kutucuğu */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Şifre</label>
            <input 
              type="password" 
              placeholder="********" 
              className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
            />
          </div>

          {/* Şifremi Unuttum */}
          <div className="flex justify-end">
            <Link href="/forgot-password" className="text-sm text-blue-600 hover:underline">
              Şifremi Unuttum?
            </Link>
          </div>

          {/* Butonlar */}
          <div className="flex flex-col gap-3 mt-6">
            <button className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition font-semibold">
              Giriş Yap
            </button>
            
            {/* Kayıt Ol Butonu */}
            <Link href="/register" className="w-full block text-center border border-blue-600 text-blue-600 py-2 rounded hover:bg-blue-50 transition font-semibold">
              Kayıt Ol
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}