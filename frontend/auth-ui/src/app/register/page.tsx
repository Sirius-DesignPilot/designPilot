import Link from 'next/link';

export default function RegisterPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-100 p-6">
      <div className="w-full max-w-md bg-white rounded-lg shadow-lg shadow-gray-700 p-8">
        <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">Kayıt Ol</h2>
        
        <form className="space-y-4">
          {/* Email Kutucuğu */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email Adresi</label>
            <input 
              type="email" 
              placeholder="ornek@email.com" 
              className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>

          {/* Şifre Kutucuğu */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Şifre</label>
            <input 
              type="password" 
              placeholder="********" 
              className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>

          {/* Şifre Tekrar Kutucuğu */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Şifreyi Tekrar Gir</label>
            <input 
              type="password" 
              placeholder="********" 
              className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>

          {/* Kayıt Ol Butonu */}
          <div className="mt-6">
            <button className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700 transition">
              Kayıt Ol
            </button>
          </div>

          {/* Giriş sayfasına geri dönüş linki */}
          <div className="text-center mt-4">
            <p className="text-sm text-gray-600">
              Zaten hesabın var mı?{' '}
              <Link href="/login" className="text-blue-600 hover:underline">
                Giriş Yap
              </Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
}