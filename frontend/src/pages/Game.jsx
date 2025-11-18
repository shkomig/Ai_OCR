import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Loader } from 'lucide-react';
import toast from 'react-hot-toast';
import { contentAPI } from '../services/api';
import Quiz from './Quiz';

export default function Game() {
  // For now, games use the same interface as quizzes
  // In a full implementation, you'd have different game types
  return <Quiz />;
}
