import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDropzone } from 'react-dropzone';
import { Upload as UploadIcon, FileImage, X, Loader } from 'lucide-react';
import toast from 'react-hot-toast';
import { documentsAPI } from '../services/api';

export default function Upload() {
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [subject, setSubject] = useState('mathematics');
  const [uploading, setUploading] = useState(false);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.webp'],
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        const file = acceptedFiles[0];
        setSelectedFile(file);

        // Create preview
        const reader = new FileReader();
        reader.onloadend = () => {
          setPreview(reader.result);
        };
        reader.readAsDataURL(file);
      }
    },
  });

  const handleUpload = async () => {
    if (!selectedFile) {
      toast.error('Please select a file to upload');
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('subject', subject);

    try {
      const response = await documentsAPI.upload(formData);
      toast.success('Document uploaded successfully!');
      navigate(`/documents/${response.data.id}`);
    } catch (error) {
      console.error('Upload error:', error);
      toast.error(error.response?.data?.detail || 'Failed to upload document');
    } finally {
      setUploading(false);
    }
  };

  const clearFile = () => {
    setSelectedFile(null);
    setPreview(null);
  };

  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">
          Upload Homework
        </h1>
        <p className="text-lg text-gray-600">
          Take a photo of your homework or upload an image to get started
        </p>
      </div>

      <div className="bg-white rounded-2xl shadow-sm p-8">
        {/* Subject Selection */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Select Subject
          </label>
          <div className="grid grid-cols-3 gap-4">
            {[
              { value: 'mathematics', label: 'Mathematics', emoji: '📐' },
              { value: 'english', label: 'English', emoji: '🔤' },
              { value: 'hebrew', label: 'עברית', emoji: 'א' },
            ].map((sub) => (
              <button
                key={sub.value}
                onClick={() => setSubject(sub.value)}
                className={`p-4 rounded-xl border-2 transition-all ${
                  subject === sub.value
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="text-3xl mb-2">{sub.emoji}</div>
                <div className="font-medium">{sub.label}</div>
              </button>
            ))}
          </div>
        </div>

        {/* File Upload Area */}
        {!selectedFile ? (
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all ${
              isDragActive
                ? 'border-primary-500 bg-primary-50'
                : 'border-gray-300 hover:border-gray-400'
            }`}
          >
            <input {...getInputProps()} />
            <UploadIcon className="w-16 h-16 mx-auto mb-4 text-gray-400" />
            <p className="text-lg font-medium text-gray-700 mb-2">
              {isDragActive
                ? 'Drop the image here'
                : 'Drag & drop homework image here'}
            </p>
            <p className="text-sm text-gray-500 mb-4">
              or click to select from your device
            </p>
            <div className="inline-flex items-center px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-colors">
              <FileImage className="w-5 h-5 mr-2" />
              Choose File
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Preview */}
            <div className="relative">
              <img
                src={preview}
                alt="Preview"
                className="w-full rounded-xl shadow-lg"
              />
              <button
                onClick={clearFile}
                className="absolute top-4 right-4 p-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors shadow-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* File Info */}
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">{selectedFile.name}</p>
                  <p className="text-sm text-gray-500">
                    {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
                <div className="text-sm text-gray-600">
                  Subject: <span className="font-medium">{subject}</span>
                </div>
              </div>
            </div>

            {/* Upload Button */}
            <button
              onClick={handleUpload}
              disabled={uploading}
              className="w-full py-4 bg-primary-600 text-white rounded-xl font-semibold hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {uploading ? (
                <>
                  <Loader className="w-5 h-5 mr-2 animate-spin" />
                  Processing...
                </>
              ) : (
                <>
                  <UploadIcon className="w-5 h-5 mr-2" />
                  Upload and Analyze
                </>
              )}
            </button>
          </div>
        )}
      </div>

      {/* Instructions */}
      <div className="mt-8 bg-blue-50 rounded-xl p-6">
        <h3 className="font-semibold text-blue-900 mb-3">Tips for Best Results:</h3>
        <ul className="space-y-2 text-sm text-blue-800">
          <li>✓ Ensure good lighting when taking photos</li>
          <li>✓ Keep the document flat and within frame</li>
          <li>✓ Supported formats: JPG, PNG, WEBP</li>
          <li>✓ Maximum file size: 10MB</li>
        </ul>
      </div>
    </div>
  );
}
