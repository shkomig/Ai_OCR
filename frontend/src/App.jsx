import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Upload from './pages/Upload'
import Documents from './pages/Documents'
import DocumentDetail from './pages/DocumentDetail'
import Game from './pages/Game'
import Quiz from './pages/Quiz'
import Review from './pages/Review'
import Dashboard from './pages/Dashboard'
import Login from './pages/Login'
import Register from './pages/Register'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="upload" element={<Upload />} />
        <Route path="documents" element={<Documents />} />
        <Route path="documents/:id" element={<DocumentDetail />} />
        <Route path="game/:id" element={<Game />} />
        <Route path="quiz/:id" element={<Quiz />} />
        <Route path="review/:id" element={<Review />} />
        <Route path="dashboard" element={<Dashboard />} />
      </Route>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
    </Routes>
  )
}

export default App
