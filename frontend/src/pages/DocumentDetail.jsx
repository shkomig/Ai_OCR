import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Loader, Gamepad2, FileQuestion, BookOpen, Plus, Play } from 'lucide-react';
import toast from 'react-hot-toast';
import { documentsAPI, contentAPI } from '../services/api';

export default function DocumentDetail() {
  const { id } = useParams();
  const [document, setDocument] = useState(null);
  const [contents, setContents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState({});

  useEffect(() => {
    loadDocument();
    loadContents();
  }, [id]);

  const loadDocument = async () => {
    try {
      const response = await documentsAPI.get(id);
      setDocument(response.data);
    } catch (error) {
      console.error('Error loading document:', error);
      toast.error('Failed to load document');
    } finally {
      setLoading(false);
    }
  };

  const loadContents = async () => {
    try {
      const response = await contentAPI.listByDocument(id);
      setContents(response.data);
    } catch (error) {
      console.error('Error loading contents:', error);
    }
  };

  const generateContent = async (type) => {
    setGenerating((prev) => ({ ...prev, [type]: true }));

    try {
      let response;
      if (type === 'game') {
        response = await contentAPI.generateGame(id);
      } else if (type === 'quiz') {
        response = await contentAPI.generateQuiz(id);
      } else if (type === 'review') {
        response = await contentAPI.generateReview(id);
      }

      toast.success(`${type.charAt(0).toUpperCase() + type.slice(1)} generated!`);
      await loadContents();
      await loadDocument();
    } catch (error) {
      console.error(`Error generating ${type}:`, error);
      toast.error(`Failed to generate ${type}`);
    } finally {
      setGenerating((prev) => ({ ...prev, [type]: false }));
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader className="w-8 h-8 animate-spin text-primary-600" />
      </div>
    );
  }

  if (!document) {
    return (
      <div className="text-center">
        <p className="text-gray-600">Document not found</p>
      </div>
    );
  }

  const gameContents = contents.filter((c) => c.content_type === 'game');
  const quizContents = contents.filter((c) => c.content_type === 'quiz');
  const reviewContents = contents.filter((c) => c.content_type === 'review');

  return (
    <div className="animate-fade-in">
      {/* Document Header */}
      <div className="bg-white rounded-2xl shadow-sm p-8 mb-8">
        <div className="flex items-start justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Document Details
            </h1>
            <p className="text-gray-600">
              Subject: <span className="font-medium capitalize">{document.subject}</span>
            </p>
            <p className="text-sm text-gray-500">
              Uploaded: {new Date(document.created_at).toLocaleString()}
            </p>
          </div>
          <span
            className={`px-3 py-1 rounded-full text-sm font-medium ${
              document.processing_status === 'completed'
                ? 'bg-green-100 text-green-800'
                : 'bg-yellow-100 text-yellow-800'
            }`}
          >
            {document.processing_status}
          </span>
        </div>

        {/* OCR Results */}
        {document.ocr_data && document.ocr_data.raw_text && (
          <div className="bg-gray-50 rounded-xl p-6">
            <h3 className="font-semibold text-gray-900 mb-3">Extracted Text:</h3>
            <p className="text-gray-700 whitespace-pre-wrap">
              {document.ocr_data.raw_text.substring(0, 500)}
              {document.ocr_data.raw_text.length > 500 && '...'}
            </p>
          </div>
        )}

        {/* Topics */}
        {document.analysis_results && document.analysis_results.topics && (
          <div className="mt-4">
            <h3 className="font-semibold text-gray-900 mb-2">Topics:</h3>
            <div className="flex flex-wrap gap-2">
              {document.analysis_results.topics.map((topic, index) => (
                <span
                  key={index}
                  className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                >
                  {topic}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Generate New Content */}
      <div className="bg-white rounded-2xl shadow-sm p-8 mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Generate Learning Content
        </h2>
        <div className="grid md:grid-cols-3 gap-4">
          <button
            onClick={() => generateContent('game')}
            disabled={generating.game || document.processing_status !== 'completed'}
            className="p-6 border-2 border-dashed border-gray-300 rounded-xl hover:border-primary-500 hover:bg-primary-50 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {generating.game ? (
              <Loader className="w-8 h-8 mx-auto mb-3 animate-spin text-primary-600" />
            ) : (
              <Gamepad2 className="w-8 h-8 mx-auto mb-3 text-green-600" />
            )}
            <h3 className="font-semibold text-gray-900 mb-1">Generate Game</h3>
            <p className="text-sm text-gray-600">Create interactive game</p>
          </button>

          <button
            onClick={() => generateContent('quiz')}
            disabled={generating.quiz || document.processing_status !== 'completed'}
            className="p-6 border-2 border-dashed border-gray-300 rounded-xl hover:border-primary-500 hover:bg-primary-50 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {generating.quiz ? (
              <Loader className="w-8 h-8 mx-auto mb-3 animate-spin text-primary-600" />
            ) : (
              <FileQuestion className="w-8 h-8 mx-auto mb-3 text-blue-600" />
            )}
            <h3 className="font-semibold text-gray-900 mb-1">Generate Quiz</h3>
            <p className="text-sm text-gray-600">Create practice quiz</p>
          </button>

          <button
            onClick={() => generateContent('review')}
            disabled={generating.review || document.processing_status !== 'completed'}
            className="p-6 border-2 border-dashed border-gray-300 rounded-xl hover:border-primary-500 hover:bg-primary-50 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {generating.review ? (
              <Loader className="w-8 h-8 mx-auto mb-3 animate-spin text-primary-600" />
            ) : (
              <BookOpen className="w-8 h-8 mx-auto mb-3 text-purple-600" />
            )}
            <h3 className="font-semibold text-gray-900 mb-1">Generate Review</h3>
            <p className="text-sm text-gray-600">Create study guide</p>
          </button>
        </div>
      </div>

      {/* Generated Content */}
      <div className="space-y-8">
        {/* Games */}
        {gameContents.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Games</h2>
            <div className="grid md:grid-cols-2 gap-4">
              {gameContents.map((content) => (
                <Link
                  key={content.id}
                  to={`/game/${content.id}`}
                  className="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-all card-hover"
                >
                  <div className="flex items-start justify-between mb-3">
                    <Gamepad2 className="w-8 h-8 text-green-600" />
                    <Play className="w-5 h-5 text-gray-400" />
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-2">
                    {content.title}
                  </h3>
                  <p className="text-sm text-gray-600 mb-3">
                    {content.description || 'Interactive learning game'}
                  </p>
                  <div className="flex items-center justify-between text-xs text-gray-500">
                    <span>Views: {content.views}</span>
                    <span>Completions: {content.completions}</span>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}

        {/* Quizzes */}
        {quizContents.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Quizzes</h2>
            <div className="grid md:grid-cols-2 gap-4">
              {quizContents.map((content) => (
                <Link
                  key={content.id}
                  to={`/quiz/${content.id}`}
                  className="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-all card-hover"
                >
                  <div className="flex items-start justify-between mb-3">
                    <FileQuestion className="w-8 h-8 text-blue-600" />
                    <Play className="w-5 h-5 text-gray-400" />
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-2">
                    {content.title}
                  </h3>
                  <p className="text-sm text-gray-600 mb-3">
                    Test your knowledge
                  </p>
                  <div className="flex items-center justify-between text-xs text-gray-500">
                    <span>Avg Score: {content.average_score.toFixed(0)}%</span>
                    <span>Completions: {content.completions}</span>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}

        {/* Reviews */}
        {reviewContents.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Study Guides</h2>
            <div className="grid md:grid-cols-2 gap-4">
              {reviewContents.map((content) => (
                <Link
                  key={content.id}
                  to={`/review/${content.id}`}
                  className="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-all card-hover"
                >
                  <div className="flex items-start justify-between mb-3">
                    <BookOpen className="w-8 h-8 text-purple-600" />
                    <Play className="w-5 h-5 text-gray-400" />
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-2">
                    {content.title}
                  </h3>
                  <p className="text-sm text-gray-600 mb-3">
                    Comprehensive study material
                  </p>
                  <div className="text-xs text-gray-500">
                    Views: {content.views}
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
