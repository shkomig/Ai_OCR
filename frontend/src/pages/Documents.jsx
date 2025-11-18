import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FileText, Loader, Trash2, Eye, Clock } from 'lucide-react';
import toast from 'react-hot-toast';
import { documentsAPI } from '../services/api';

export default function Documents() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const response = await documentsAPI.list();
      setDocuments(response.data);
    } catch (error) {
      console.error('Error loading documents:', error);
      toast.error('Failed to load documents');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this document?')) return;

    try {
      await documentsAPI.delete(id);
      toast.success('Document deleted');
      setDocuments(documents.filter((doc) => doc.id !== id));
    } catch (error) {
      console.error('Error deleting document:', error);
      toast.error('Failed to delete document');
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'processing':
        return 'bg-yellow-100 text-yellow-800';
      case 'error':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getSubjectEmoji = (subject) => {
    switch (subject) {
      case 'mathematics':
        return '📐';
      case 'english':
        return '🔤';
      case 'hebrew':
        return 'א';
      default:
        return '📚';
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader className="w-8 h-8 animate-spin text-primary-600" />
      </div>
    );
  }

  return (
    <div className="animate-fade-in">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">My Documents</h1>
          <p className="text-lg text-gray-600">
            {documents.length} document{documents.length !== 1 ? 's' : ''} uploaded
          </p>
        </div>
        <Link
          to="/upload"
          className="px-6 py-3 bg-primary-600 text-white rounded-xl font-medium hover:bg-primary-700 transition-colors"
        >
          Upload New
        </Link>
      </div>

      {documents.length === 0 ? (
        <div className="bg-white rounded-2xl shadow-sm p-12 text-center">
          <FileText className="w-16 h-16 mx-auto mb-4 text-gray-300" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            No documents yet
          </h3>
          <p className="text-gray-600 mb-6">
            Upload your first homework document to get started
          </p>
          <Link
            to="/upload"
            className="inline-flex items-center px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-colors"
          >
            Upload Document
          </Link>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {documents.map((doc) => (
            <div
              key={doc.id}
              className="bg-white rounded-xl shadow-sm hover:shadow-md transition-all overflow-hidden card-hover"
            >
              {/* Document Image */}
              <div className="aspect-video bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center">
                <div className="text-6xl">{getSubjectEmoji(doc.subject)}</div>
              </div>

              {/* Content */}
              <div className="p-6">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <span
                      className={`inline-block px-2 py-1 text-xs font-medium rounded ${getStatusColor(
                        doc.processing_status
                      )}`}
                    >
                      {doc.processing_status}
                    </span>
                  </div>
                  <span className="text-sm text-gray-500 capitalize">
                    {doc.subject}
                  </span>
                </div>

                <div className="flex items-center text-sm text-gray-500 mb-4">
                  <Clock className="w-4 h-4 mr-1" />
                  {new Date(doc.created_at).toLocaleDateString()}
                </div>

                {/* Stats */}
                {doc.processing_status === 'completed' && (
                  <div className="grid grid-cols-3 gap-2 mb-4 text-center text-xs">
                    <div className="bg-blue-50 rounded p-2">
                      <div className="font-semibold text-blue-900">
                        {doc.generated_content?.games?.length || 0}
                      </div>
                      <div className="text-blue-600">Games</div>
                    </div>
                    <div className="bg-green-50 rounded p-2">
                      <div className="font-semibold text-green-900">
                        {doc.generated_content?.quizzes?.length || 0}
                      </div>
                      <div className="text-green-600">Quizzes</div>
                    </div>
                    <div className="bg-purple-50 rounded p-2">
                      <div className="font-semibold text-purple-900">
                        {doc.generated_content?.review_materials?.length || 0}
                      </div>
                      <div className="text-purple-600">Reviews</div>
                    </div>
                  </div>
                )}

                {/* Actions */}
                <div className="flex gap-2">
                  <Link
                    to={`/documents/${doc.id}`}
                    className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700 transition-colors flex items-center justify-center"
                  >
                    <Eye className="w-4 h-4 mr-1" />
                    View
                  </Link>
                  <button
                    onClick={() => handleDelete(doc.id)}
                    className="px-4 py-2 bg-red-50 text-red-600 rounded-lg text-sm font-medium hover:bg-red-100 transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
