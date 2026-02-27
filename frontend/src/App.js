import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import ErrorBoundary from './components/ErrorBoundary';
import PrivateRoute from './components/PrivateRoute';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import CareerRecommendations from './pages/CareerRecommendations';
import CoverLetterGenerator from './pages/CoverLetterGenerator';
import JobSearch from './pages/JobSearch';
import HomePage from './pages/HomePage';
import SalaryPredictor from './pages/SalaryPredictor';
import InterviewPrep from './pages/InterviewPrep';
import CareerPath from './pages/CareerPath';
import NotFound from './pages/NotFound';
import './styles/index.css';

function App() {
  return (
    <ErrorBoundary>
      <Router>
        <AuthProvider>
          <ThemeProvider>
            <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/home"
              element={
                <PrivateRoute>
                  <HomePage />
                </PrivateRoute>
              }
            />
            <Route
              path="/dashboard"
              element={
                <PrivateRoute>
                  <Dashboard />
                </PrivateRoute>
              }
            />
            <Route
              path="/career-recommendations"
              element={
                <PrivateRoute>
                  <CareerRecommendations />
                </PrivateRoute>
              }
            />
            <Route
              path="/cover-letter-generator"
              element={
                <PrivateRoute>
                  <CoverLetterGenerator />
                </PrivateRoute>
              }
            />
            <Route
              path="/job-search"
              element={
                <PrivateRoute>
                  <JobSearch />
                </PrivateRoute>
              }
            />
            <Route
              path="/salary-predictor"
              element={
                <PrivateRoute>
                  <SalaryPredictor />
                </PrivateRoute>
              }
            />
            <Route
              path="/interview-prep"
              element={
                <PrivateRoute>
                  <InterviewPrep />
                </PrivateRoute>
              }
            />
            <Route
              path="/career-path"
              element={
                <PrivateRoute>
                  <CareerPath />
                </PrivateRoute>
              }
            />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </ThemeProvider>
      </AuthProvider>
    </Router>
  </ErrorBoundary>
  );
}

export default App;
