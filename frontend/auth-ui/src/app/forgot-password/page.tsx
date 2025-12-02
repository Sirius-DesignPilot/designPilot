import Link from 'next/link';

export default function ForgotPasswordPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-100 p-6">
      <div className="w-full max-w-md bg-white rounded-lg shadow-lg shadow-gray-700 p-8 text-black">
        <h2 className="text-2xl font-bold text-center text-gray-800 mb-4">Şifremi Unuttum</h2>
        
        <p className="text-sm text-gray-600 text-center mb-6">
          Hesabınıza kayıtlı e-posta adresinizi aşağıya girin. Size şifrenizi sıfırlamanız için bir bağlantı göndereceğiz.
        </p>
        
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

          {/* Gönder Butonu */}
          <div className="mt-6">
            <button className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition font-semibold">
              Sıfırlama Bağlantısı Gönder
            </button>
          </div>

          {/* Giriş sayfasına geri dönüş */}
          <div className="text-center mt-4">
            <Link href="/login" className="text-sm text-gray-500 hover:text-blue-600 hover:underline flex items-center justify-center gap-1">
              <span>←</span> Giriş ekranına dön
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}