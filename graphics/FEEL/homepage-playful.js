window.PlayfulHomepage = () => {
  return (
    <div className="min-h-screen bg-rose-50">
      {/* Your existing JSX code here */}
    </div>
  );
};
const PlayfulHomepage = () => {
  return (
    <div className="min-h-screen bg-rose-50">
      {/* Navigation */}
      <nav className="bg-white/80 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="text-2xl font-arabic text-rose-900">تَشْكِيل</div>
            <div className="flex gap-6">
              <button className="rounded-full bg-rose-100 p-3 hover:bg-rose-200 transition-colors">
                <svg className="w-5 h-5 text-rose-700" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle cx="12" cy="12" r="10" strokeWidth="2"/>
                  <path d="M12 16v-4M12 8h.01" strokeWidth="2" strokeLinecap="round"/>
                </svg>
              </button>
              <button className="rounded-full bg-rose-100 p-3 hover:bg-rose-200 transition-colors">
                <svg className="w-5 h-5 text-rose-700" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M12 6V4m0 2a6 6 0 100 12 6 6 0 000-12z" strokeWidth="2" strokeLinecap="round"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-6 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-arabic font-bold text-rose-900 mb-6">
            Arabic Text Diacritization
          </h1>
          <p className="text-xl text-rose-700 max-w-2xl mx-auto leading-relaxed">
            Bring your Arabic text to life with beautiful diacritical marks
          </p>
        </div>

        {/* Mode Cards with Playful Animation */}
        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {/* Training Card */}
          <div className="group relative">
            <div className="absolute inset-0 bg-gradient-to-r from-rose-200 to-rose-300 rounded-2xl transform rotate-2 transition-transform group-hover:rotate-1" />
            <div className="relative bg-white rounded-2xl p-8 shadow-sm hover:shadow-md transition-all">
              <div className="w-20 h-20 mx-auto mb-6 bg-rose-100 rounded-full flex items-center justify-center">
                <svg className="w-10 h-10 text-rose-600" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-rose-900 text-center mb-4">Training Mode</h2>
              <p className="text-rose-700 text-center mb-8">
                Perfect your skills with guided exercises and instant feedback
              </p>
              <button className="w-full bg-rose-600 text-white py-4 rounded-xl font-semibold hover:bg-rose-700 transform hover:-translate-y-0.5 transition-all">
                Begin Training Journey
              </button>
            </div>
          </div>

          {/* Diacritization Card */}
          <div className="group relative">
            <div className="absolute inset-0 bg-gradient-to-r from-rose-300 to-rose-400 rounded-2xl transform -rotate-2 transition-transform group-hover:-rotate-1" />
            <div className="relative bg-white rounded-2xl p-8 shadow-sm hover:shadow-md transition-all">
              <div className="w-20 h-20 mx-auto mb-6 bg-rose-100 rounded-full flex items-center justify-center">
                <svg className="w-10 h-10 text-rose-600" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-rose-900 text-center mb-4">Diacritization Mode</h2>
              <p className="text-rose-700 text-center mb-8">
                Add beautiful diacritical marks to your Arabic text
              </p>
              <button className="w-full bg-rose-600 text-white py-4 rounded-xl font-semibold hover:bg-rose-700 transform hover:-translate-y-0.5 transition-all">
                Start Diacritizing
              </button>
            </div>
          </div>
        </div>

        {/* Quick Navigation */}
        <div className="mt-16 flex justify-center gap-6 text-rose-700">
          <a href="/about" className="hover:text-rose-900 transition-colors">About</a>
          <span className="text-rose-300">•</span>
          <a href="/help" className="hover:text-rose-900 transition-colors">Help</a>
          <span className="text-rose-300">•</span>
          <a href="/contact" className="hover:text-rose-900 transition-colors">Contact</a>
        </div>
      </main>
    </div>
  );
};

