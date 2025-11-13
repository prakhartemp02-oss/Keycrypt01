/** Main landing page for KeyCrypt */

'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { fadeIn, slideUp, floating, pulse } from '../lib/animations';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Navigation */}
      <motion.nav
        className="flex justify-between items-center p-6 max-w-7xl mx-auto"
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex items-center gap-2">
          <span className="text-3xl">🔐</span>
          <h1 className="text-2xl font-bold text-gray-800 dark:text-white">KeyCrypt</h1>
        </div>
        <Link
          href="/levels"
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition-colors duration-200"
        >
          Play Now
        </Link>
      </motion.nav>

      {/* Hero Section */}
      <motion.section
        className="max-w-7xl mx-auto px-6 py-20 text-center"
        variants={fadeIn}
        initial="initial"
        animate="animate"
        transition={{ delay: 0.2 }}
      >
        <motion.div
          className="mb-6"
          variants={floating}
          animate="animate"
        >
          <span className="text-6xl">🔐</span>
        </motion.div>

        <h2 className="text-5xl md:text-7xl font-bold text-gray-800 dark:text-white mb-6">
          Learn Cryptography
          <br />
          <span className="text-blue-600 dark:text-blue-400">Through Play</span>
        </h2>

        <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
          Master the art of encryption through interactive Wordle-like puzzles.
          Journey from ancient ciphers like Caesar to modern encryption like RSA.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Link
            href="/levels"
            className="px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold text-lg transition-all duration-200 transform hover:scale-105"
          >
            Start Learning
          </Link>
          <button
            className="px-8 py-4 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-800 dark:text-white rounded-lg font-semibold text-lg border border-gray-300 dark:border-gray-600 transition-all duration-200"
          >
            Learn More
          </button>
        </div>
      </motion.section>

      {/* Features Section */}
      <motion.section
        className="max-w-7xl mx-auto px-6 py-20"
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        viewport={{ once: true }}
      >
        <h3 className="text-3xl md:text-4xl font-bold text-center text-gray-800 dark:text-white mb-12">
          Why Learn with KeyCrypt?
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <motion.div
            className="text-center p-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg"
            whileHover={{ y: -5 }}
            transition={{ type: 'spring', stiffness: 100 }}
          >
            <div className="text-4xl mb-4">🎮</div>
            <h4 className="text-xl font-semibold text-gray-800 dark:text-white mb-2">
              Interactive Gameplay
            </h4>
            <p className="text-gray-600 dark:text-gray-300">
              Learn by doing with hands-on puzzle solving and real-time feedback.
            </p>
          </motion.div>

          <motion.div
            className="text-center p-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg"
            whileHover={{ y: -5 }}
            transition={{ type: 'spring', stiffness: 100 }}
          >
            <div className="text-4xl mb-4">🏛️</div>
            <h4 className="text-xl font-semibold text-gray-800 dark:text-white mb-2">
              Historical Context
            </h4>
            <p className="text-gray-600 dark:text-gray-300">
              Understand the evolution of cryptography from ancient times to modern day.
            </p>
          </motion.div>

          <motion.div
            className="text-center p-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg"
            whileHover={{ y: -5 }}
            transition={{ type: 'spring', stiffness: 100 }}
          >
            <div className="text-4xl mb-4">🔒</div>
            <h4 className="text-xl font-semibold text-gray-800 dark:text-white mb-2">
              Real Security
            </h4>
            <p className="text-gray-600 dark:text-gray-300">
              Learn principles used in actual secure communication systems.
            </p>
          </motion.div>
        </div>
      </motion.section>

      {/* Level Preview */}
      <motion.section
        className="max-w-7xl mx-auto px-6 py-20"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        transition={{ duration: 0.6 }}
        viewport={{ once: true }}
      >
        <h3 className="text-3xl md:text-4xl font-bold text-center text-gray-800 dark:text-white mb-12">
          9 Levels of Cryptographic Mastery
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          {[
            { name: 'Caesar Cipher', level: 1, icon: '📜' },
            { name: 'Monoalphabetic Substitution', level: 2, icon: '🔤' },
            { name: 'Playfair Cipher', level: 3, icon: '🏛️' },
            { name: 'Hill Cipher', level: 4, icon: '📊' },
            { name: 'Rail Fence', level: 5, icon: '🚂' },
            { name: 'Vigenère Cipher', level: 6, icon: '🔑' },
            { name: 'One-Time Pad', level: 7, icon: '🎯' },
            { name: 'DES/3DES', level: 8, icon: '🔐' },
            { name: 'RSA', level: 9, icon: '💻' },
          ].map((item) => (
            <motion.div
              key={item.level}
              className="flex items-center gap-3 p-4 bg-white dark:bg-gray-800 rounded-lg shadow"
              variants={slideUp}
              whileHover={{ scale: 1.02 }}
            >
              <div className="text-2xl">{item.icon}</div>
              <div>
                <div className="text-sm text-gray-500 dark:text-gray-400">Level {item.level}</div>
                <div className="font-semibold text-gray-800 dark:text-white">{item.name}</div>
              </div>
            </motion.div>
          ))}
        </div>

        <div className="text-center">
          <Link
            href="/levels"
            className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition-all duration-200 transform hover:scale-105"
          >
            View All Levels
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </Link>
        </div>
      </motion.section>

      {/* Call to Action */}
      <motion.section
        className="max-w-7xl mx-auto px-6 py-20 text-center"
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        viewport={{ once: true }}
      >
        <motion.div
          className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-12 text-white"
          variants={pulse}
          animate="animate"
        >
          <h3 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to Master Cryptography?
          </h3>
          <p className="text-xl mb-8 opacity-90">
            Start your journey from beginner to crypto expert today.
          </p>
          <Link
            href="/levels"
            className="inline-block px-8 py-4 bg-white text-blue-600 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-all duration-200 transform hover:scale-105"
          >
            Get Started Free
          </Link>
        </motion.div>
      </motion.section>

      {/* Footer */}
      <footer className="mt-20 py-8 border-t border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-6 text-center text-gray-600 dark:text-gray-300">
          <p>© 2024 KeyCrypt. Learn cryptography through play.</p>
        </div>
      </footer>
    </div>
  );
}
