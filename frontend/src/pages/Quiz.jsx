import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Loader, CheckCircle, XCircle, Trophy } from 'lucide-react';
import toast from 'react-hot-toast';
import { contentAPI, progressAPI } from '../services/api';

export default function Quiz() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);
  const [score, setScore] = useState(0);
  const [startTime] = useState(Date.now());

  useEffect(() => {
    loadContent();
  }, [id]);

  const loadContent = async () => {
    try {
      const response = await contentAPI.get(id);
      setContent(response.data);
    } catch (error) {
      console.error('Error loading quiz:', error);
      toast.error('Failed to load quiz');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = (questionId, answer) => {
    setAnswers((prev) => ({ ...prev, [questionId]: answer }));
  };

  const submitQuiz = async () => {
    const questions = content.content_json.questions;
    const answerSubmissions = questions.map((q) => ({
      question_id: q.id,
      user_answer: answers[q.id] || '',
      time_spent_seconds: Math.floor((Date.now() - startTime) / 1000 / questions.length),
    }));

    try {
      const response = await progressAPI.submit({
        content_id: id,
        answers: answerSubmissions,
        total_time_spent: Math.floor((Date.now() - startTime) / 1000),
      });

      setScore(response.data.score);
      setShowResults(true);
      toast.success('Quiz submitted!');
    } catch (error) {
      console.error('Error submitting quiz:', error);
      toast.error('Failed to submit quiz');
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

  const questions = content.content_json.questions || [];
  const question = questions[currentQuestion];

  if (showResults) {
    return (
      <div className="max-w-2xl mx-auto text-center animate-fade-in">
        <div className="bg-white rounded-2xl shadow-sm p-12">
          <Trophy className="w-20 h-20 mx-auto mb-6 text-yellow-500" />
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Quiz Complete!</h1>
          <div className="text-6xl font-bold text-primary-600 mb-2">{score.toFixed(0)}%</div>
          <p className="text-xl text-gray-600 mb-8">
            {score >= 90 ? 'Excellent!' : score >= 70 ? 'Great job!' : 'Keep practicing!'}
          </p>
          <button
            onClick={() => navigate('/documents')}
            className="px-8 py-3 bg-primary-600 text-white rounded-xl font-semibold hover:bg-primary-700 transition-colors"
          >
            Back to Documents
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto animate-fade-in">
      <div className="bg-white rounded-2xl shadow-sm p-8">
        {/* Progress */}
        <div className="mb-6">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>Question {currentQuestion + 1} of {questions.length}</span>
            <span>{Math.round(((currentQuestion + 1) / questions.length) * 100)}%</span>
          </div>
          <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-primary-600 transition-all"
              style={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
            />
          </div>
        </div>

        {/* Question */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">{question.question}</h2>

          {question.type === 'multiple_choice' && (
            <div className="space-y-3">
              {question.options.map((option, index) => (
                <button
                  key={index}
                  onClick={() => handleAnswer(question.id, option)}
                  className={`w-full p-4 rounded-xl border-2 text-left transition-all ${
                    answers[question.id] === option
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  {option}
                </button>
              ))}
            </div>
          )}

          {question.type === 'true_false' && (
            <div className="grid grid-cols-2 gap-4">
              {['True', 'False'].map((option) => (
                <button
                  key={option}
                  onClick={() => handleAnswer(question.id, option)}
                  className={`p-6 rounded-xl border-2 font-semibold transition-all ${
                    answers[question.id] === option
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  {option}
                </button>
              ))}
            </div>
          )}

          {question.type === 'short_answer' && (
            <input
              type="text"
              value={answers[question.id] || ''}
              onChange={(e) => handleAnswer(question.id, e.target.value)}
              placeholder="Type your answer..."
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:outline-none"
            />
          )}
        </div>

        {/* Navigation */}
        <div className="flex justify-between">
          <button
            onClick={() => setCurrentQuestion(Math.max(0, currentQuestion - 1))}
            disabled={currentQuestion === 0}
            className="px-6 py-3 border border-gray-300 rounded-xl font-medium hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>

          {currentQuestion < questions.length - 1 ? (
            <button
              onClick={() => setCurrentQuestion(currentQuestion + 1)}
              className="px-6 py-3 bg-primary-600 text-white rounded-xl font-medium hover:bg-primary-700 transition-colors"
            >
              Next
            </button>
          ) : (
            <button
              onClick={submitQuiz}
              className="px-6 py-3 bg-green-600 text-white rounded-xl font-medium hover:bg-green-700 transition-colors"
            >
              Submit Quiz
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
