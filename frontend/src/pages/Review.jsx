import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Loader, BookOpen, CheckCircle } from 'lucide-react';
import toast from 'react-hot-toast';
import { contentAPI } from '../services/api';

export default function Review() {
  const { id } = useParams();
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadContent();
  }, [id]);

  const loadContent = async () => {
    try {
      const response = await contentAPI.get(id);
      setContent(response.data);
    } catch (error) {
      console.error('Error loading review material:', error);
      toast.error('Failed to load review material');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader className="w-8 h-8 animate-spin text-primary-600" />
      </div>
    );
  }

  if (!content) return null;

  const reviewData = content.content_json;

  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl p-8 text-white mb-8">
        <BookOpen className="w-12 h-12 mb-4" />
        <h1 className="text-4xl font-bold mb-2">{reviewData.title}</h1>
        <p className="text-blue-100">Subject: {reviewData.subject}</p>
        <p className="text-sm text-blue-200 mt-2">
          Estimated study time: {reviewData.estimated_study_time_minutes} minutes
        </p>
      </div>

      {/* Sections */}
      <div className="space-y-6">
        {reviewData.sections?.map((section, index) => (
          <div key={index} className="bg-white rounded-2xl shadow-sm p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">{section.topic}</h2>
            <p className="text-gray-700 mb-6">{section.summary}</p>

            {/* Key Points */}
            {section.key_points && section.key_points.length > 0 && (
              <div className="mb-6">
                <h3 className="font-semibold text-gray-900 mb-3">Key Points:</h3>
                <ul className="space-y-2">
                  {section.key_points.map((point, i) => (
                    <li key={i} className="flex items-start">
                      <CheckCircle className="w-5 h-5 text-green-600 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-gray-700">{point}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Examples */}
            {section.examples && section.examples.length > 0 && (
              <div className="mb-6">
                <h3 className="font-semibold text-gray-900 mb-3">Examples:</h3>
                {section.examples.map((example, i) => (
                  <div key={i} className="bg-blue-50 rounded-xl p-4 mb-3">
                    <p className="font-medium text-blue-900 mb-2">{example.problem}</p>
                    <p className="text-sm text-blue-800 whitespace-pre-wrap mb-2">{example.solution}</p>
                    <p className="text-sm text-blue-600 italic">{example.explanation}</p>
                  </div>
                ))}
              </div>
            )}

            {/* Common Mistakes */}
            {section.common_mistakes && section.common_mistakes.length > 0 && (
              <div className="mb-6">
                <h3 className="font-semibold text-gray-900 mb-3">Common Mistakes to Avoid:</h3>
                <ul className="space-y-2">
                  {section.common_mistakes.map((mistake, i) => (
                    <li key={i} className="text-red-700 bg-red-50 rounded-lg p-3">
                      ⚠️ {mistake}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Memory Aids */}
            {section.memory_aids && section.memory_aids.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Memory Aids:</h3>
                <div className="space-y-2">
                  {section.memory_aids.map((aid, i) => (
                    <p key={i} className="text-purple-700 bg-purple-50 rounded-lg p-3">
                      💡 {aid}
                    </p>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}

        {/* Quick Review Questions */}
        {reviewData.quick_review_questions && reviewData.quick_review_questions.length > 0 && (
          <div className="bg-white rounded-2xl shadow-sm p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Quick Review Questions</h2>
            <div className="space-y-4">
              {reviewData.quick_review_questions.map((q, index) => (
                <details key={index} className="bg-gray-50 rounded-xl p-4">
                  <summary className="font-medium text-gray-900 cursor-pointer">
                    {index + 1}. {q.question}
                  </summary>
                  <p className="mt-3 text-gray-700 pl-4">{q.answer}</p>
                </details>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
