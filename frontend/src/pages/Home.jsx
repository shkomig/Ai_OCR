import { Link } from 'react-router-dom';
import { Upload, Brain, Gamepad2, BarChart3, Camera, Sparkles } from 'lucide-react';

export default function Home() {
  const features = [
    {
      icon: Camera,
      title: 'Smart OCR',
      description: 'Capture homework with your smartphone camera. Advanced OCR extracts text instantly.',
      color: 'bg-blue-500',
    },
    {
      icon: Brain,
      title: 'AI Analysis',
      description: 'Claude AI analyzes content, identifies topics, and creates personalized learning paths.',
      color: 'bg-purple-500',
    },
    {
      icon: Gamepad2,
      title: 'Interactive Games',
      description: 'Transform homework into engaging games, quizzes, and interactive challenges.',
      color: 'bg-green-500',
    },
    {
      icon: BarChart3,
      title: 'Progress Tracking',
      description: 'Monitor learning progress, scores, and receive AI-powered feedback.',
      color: 'bg-orange-500',
    },
  ];

  return (
    <div className="animate-fade-in">
      {/* Hero Section */}
      <div className="relative overflow-hidden bg-gradient-to-br from-primary-600 via-purple-600 to-pink-500 rounded-3xl p-12 mb-12 text-white">
        <div className="absolute top-0 right-0 -mt-16 -mr-16 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 left-0 -mb-16 -ml-16 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>

        <div className="relative z-10 max-w-3xl">
          <div className="flex items-center mb-4">
            <Sparkles className="w-8 h-8 mr-2" />
            <span className="text-sm font-semibold uppercase tracking-wider">
              AI-Powered Learning
            </span>
          </div>
          <h1 className="text-5xl font-bold mb-6 leading-tight">
            Transform Homework into
            <br />
            <span className="text-yellow-300">Interactive Adventures</span>
          </h1>
          <p className="text-xl mb-8 text-blue-100 max-w-2xl">
            Upload your homework, let AI analyze it, and instantly get engaging games,
            quizzes, and personalized study materials. Learning has never been this fun!
          </p>
          <div className="flex flex-wrap gap-4">
            <Link
              to="/upload"
              className="inline-flex items-center px-8 py-4 bg-white text-primary-700 rounded-xl font-semibold hover:bg-blue-50 transition-all transform hover:scale-105 shadow-lg"
            >
              <Upload className="w-5 h-5 mr-2" />
              Upload Homework
            </Link>
            <Link
              to="/documents"
              className="inline-flex items-center px-8 py-4 bg-white/20 backdrop-blur-sm text-white rounded-xl font-semibold hover:bg-white/30 transition-all border border-white/30"
            >
              View My Documents
            </Link>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="mb-12">
        <h2 className="text-3xl font-bold text-gray-900 mb-2 text-center">
          How It Works
        </h2>
        <p className="text-lg text-gray-600 mb-8 text-center max-w-2xl mx-auto">
          Four simple steps to transform your homework into an interactive learning experience
        </p>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div
                key={index}
                className="bg-white rounded-2xl p-6 shadow-sm hover:shadow-lg transition-all card-hover animate-slide-up"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className={`${feature.color} w-12 h-12 rounded-xl flex items-center justify-center mb-4`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Supported Subjects */}
      <div className="bg-white rounded-2xl p-8 shadow-sm">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
          Supported Subjects
        </h2>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="text-center p-6 bg-blue-50 rounded-xl">
            <div className="text-4xl mb-3">📐</div>
            <h3 className="font-semibold text-lg mb-2">Mathematics</h3>
            <p className="text-sm text-gray-600">
              Algebra, Geometry, Calculus, and more
            </p>
          </div>
          <div className="text-center p-6 bg-green-50 rounded-xl">
            <div className="text-4xl mb-3">🔤</div>
            <h3 className="font-semibold text-lg mb-2">English</h3>
            <p className="text-sm text-gray-600">
              Reading, Writing, Grammar, Vocabulary
            </p>
          </div>
          <div className="text-center p-6 bg-purple-50 rounded-xl hebrew">
            <div className="text-4xl mb-3">א</div>
            <h3 className="font-semibold text-lg mb-2">עברית</h3>
            <p className="text-sm text-gray-600">
              קריאה, כתיבה, דקדוק ואוצר מילים
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="mt-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white text-center">
        <h2 className="text-3xl font-bold mb-4">Ready to Get Started?</h2>
        <p className="text-xl mb-6 text-blue-100">
          Upload your first homework document and experience the future of learning
        </p>
        <Link
          to="/upload"
          className="inline-flex items-center px-8 py-4 bg-white text-purple-700 rounded-xl font-semibold hover:bg-blue-50 transition-all transform hover:scale-105 shadow-lg"
        >
          <Upload className="w-5 h-5 mr-2" />
          Start Learning Now
        </Link>
      </div>
    </div>
  );
}
