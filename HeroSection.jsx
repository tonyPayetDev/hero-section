import React, { useRef, useState, useEffect } from 'react';
import { motion } from 'framer-motion';

export default function HeroSection() {
  const portraitRef = useRef(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [isHovering, setIsHovering] = useState(false);

  const handleMouseMove = (e) => {
    if (!portraitRef.current) return;
    const rect = portraitRef.current.getBoundingClientRect();
    setMousePos({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    });
  };

  const handleMouseEnter = () => setIsHovering(true);
  const handleMouseLeave = () => setIsHovering(false);

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1, delayChildren: 0.2 },
    },
  };

  const leftColumnVariants = {
    hidden: { opacity: 0, x: -60 },
    visible: { opacity: 1, x: 0, transition: { duration: 0.6, ease: 'easeOut' } },
  };

  const dataPointVariants = {
    hidden: { opacity: 0, scale: 0.8 },
    visible: {
      opacity: 1,
      scale: 1,
      transition: { duration: 0.5, ease: 'easeOut' },
    },
  };

  // Floating animation for portrait
  const floatingVariants = {
    initial: { y: 0 },
    animate: {
      y: [-8, 0],
      transition: { duration: 3, repeat: Infinity, ease: 'easeInOut' },
    },
  };

  return (
    <div
      className="w-full h-screen overflow-hidden"
      style={{
        background: `radial-gradient(circle at center, #FF6B00 0%, #4A0000 100%)`,
      }}
    >
      {/* NAVBAR */}
      <nav className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-8 py-6">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-white opacity-80"></div>
          <span className="text-white font-bold text-lg">Tony Payet</span>
        </div>

        {/* Center Links */}
        <div className="hidden lg:flex gap-12 absolute left-1/2 transform -translate-x-1/2">
          {['Services', 'Case Studies', 'Automation', 'Pricing', 'Live Demo'].map(
            (link) => (
              <motion.a
                key={link}
                href="#"
                className="text-white text-xs uppercase tracking-widest relative group"
                whileHover={{ opacity: 0.8 }}
              >
                {link}
                <motion.span
                  className="absolute bottom-0 left-0 right-0 h-0.5 bg-white"
                  initial={{ scaleX: 0 }}
                  whileHover={{ scaleX: 1 }}
                  transition={{ duration: 0.2 }}
                />
              </motion.a>
            )
          )}
        </div>

        {/* Connect Button */}
        <motion.button
          whileHover={{ backgroundColor: 'white', color: 'black', boxShadow: '0 0 20px rgba(255,255,255,0.3)' }}
          transition={{ duration: 0.2 }}
          className="px-6 py-2 border border-white text-white rounded-full text-xs uppercase tracking-wider font-semibold hover:shadow-lg"
        >
          Connect
        </motion.button>
      </nav>

      {/* MAIN CONTENT */}
      <div className="h-full pt-24 grid grid-cols-1 lg:grid-cols-3 gap-8 px-8 lg:px-16">

        {/* LEFT COLUMN - Text Content */}
        <motion.div
          className="flex flex-col justify-center col-span-1"
          variants={leftColumnVariants}
          initial="hidden"
          animate="visible"
        >
          {/* Supertitle */}
          <motion.p
            className="text-white opacity-70 text-sm italic font-light mb-6"
            style={{ fontFamily: "'Space Mono', monospace" }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 0.7 }}
            transition={{ delay: 0.3 }}
          >
            Gateway to your automated business
          </motion.p>

          {/* H1 Title */}
          <motion.h1
            className="text-white font-black text-5xl lg:text-7xl leading-tight mb-6"
            style={{ fontFamily: "'Space Grotesk', sans-serif" }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.6 }}
          >
            The man who<br />
            automates<br />
            your growth
          </motion.h1>

          {/* Description */}
          <motion.p
            className="text-white opacity-60 text-sm mb-8 max-w-md leading-relaxed"
            style={{ fontFamily: "'Space Mono', monospace" }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 0.6 }}
            transition={{ delay: 0.5 }}
          >
            Where n8n workflows, AI pipelines, and human strategy align. Not a tool. Not an agency. Something powerfully between.
          </motion.p>

          {/* CTA Button */}
          <motion.button
            whileHover={{
              scale: 1.05,
              boxShadow: '0 0 30px rgba(255, 107, 0, 0.5)',
            }}
            className="w-fit px-8 py-3 bg-white text-black rounded-full font-semibold text-sm uppercase tracking-wide"
          >
            Book a Call
          </motion.button>
        </motion.div>

        {/* CENTER COLUMN - Portrait with Hover Interactions */}
        <motion.div
          ref={portraitRef}
          className="hidden lg:flex items-center justify-center col-span-1 relative"
          onMouseMove={handleMouseMove}
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
          variants={floatingVariants}
          initial="initial"
          animate="animate"
        >
          {/* Portrait Image Container */}
          <div className="relative w-full h-full max-w-sm">
            {/* Normal portrait */}
            <div
              className="w-full h-full rounded-lg overflow-hidden"
              style={{
                maskImage: isHovering
                  ? `radial-gradient(circle 150px at ${mousePos.x}px ${mousePos.y}px, transparent 0%, black 100%)`
                  : 'linear-gradient(to right, transparent 0%, black 30%, black 70%, transparent 100%)',
              }}
            >
              {/* Placeholder for user photo */}
              <div className="w-full h-full bg-gradient-to-b from-orange-500 via-purple-600 to-gray-900 flex items-center justify-center">
                <span className="text-white text-opacity-50 text-lg">Your Photo Here</span>
              </div>
            </div>

            {/* Cyberpunk HUD overlay (revealed on hover) */}
            {isHovering && (
              <motion.div
                className="absolute inset-0 rounded-lg overflow-hidden"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
                style={{
                  maskImage: `radial-gradient(circle 150px at ${mousePos.x}px ${mousePos.y}px, black 0%, transparent 100%)`,
                }}
              >
                <div
                  className="w-full h-full"
                  style={{
                    filter: 'hue-rotate(180deg) contrast(1.4) brightness(1.2)',
                    background: 'linear-gradient(135deg, #FF6B00 0%, #00d4ff 100%)',
                    backgroundBlendMode: 'multiply',
                  }}
                >
                  <div className="w-full h-full bg-gradient-to-b from-orange-500 via-purple-600 to-gray-900 opacity-70"></div>
                </div>
              </motion.div>
            )}

            {/* Glow ring around cursor */}
            {isHovering && (
              <motion.div
                className="absolute rounded-full pointer-events-none"
                style={{
                  width: '300px',
                  height: '300px',
                  left: `${mousePos.x - 150}px`,
                  top: `${mousePos.y - 150}px`,
                  border: '1px solid #FF6B00',
                  boxShadow: '0 0 20px #FF6B00, inset 0 0 20px #FF6B00',
                }}
              />
            )}

            {/* HUD Data Tags */}
            {isHovering && (
              <>
                <motion.div
                  className="absolute top-8 left-8 text-white text-xs p-3 border border-white border-opacity-30 rounded bg-black bg-opacity-50 backdrop-blur-sm"
                  style={{ fontFamily: "'Space Mono', monospace" }}
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 }}
                >
                  <div>ID: TONY_PAYET</div>
                </motion.div>

                <motion.div
                  className="absolute top-8 right-8 text-white text-xs p-3 border border-white border-opacity-30 rounded bg-black bg-opacity-50 backdrop-blur-sm"
                  style={{ fontFamily: "'Space Mono', monospace" }}
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.15 }}
                >
                  <div>STATUS: ONLINE ●</div>
                </motion.div>

                <motion.div
                  className="absolute bottom-8 left-8 text-white text-xs p-3 border border-white border-opacity-30 rounded bg-black bg-opacity-50 backdrop-blur-sm"
                  style={{ fontFamily: "'Space Mono', monospace" }}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                >
                  <div>SKILL: AI AUTOMATION</div>
                </motion.div>

                <motion.div
                  className="absolute bottom-8 right-8 text-white text-xs p-3 border border-white border-opacity-30 rounded bg-black bg-opacity-50 backdrop-blur-sm"
                  style={{ fontFamily: "'Space Mono', monospace" }}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.25 }}
                >
                  <div>LVL: EXPERT ██████░░</div>
                </motion.div>
              </>
            )}
          </div>
        </motion.div>

        {/* RIGHT COLUMN - Radar UI Data */}
        <motion.div
          className="hidden lg:flex items-center justify-end col-span-1"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <div className="relative w-full h-96">
            {/* SVG Radar */}
            <svg
              className="absolute -right-32 top-1/2 transform -translate-y-1/2"
              width="400"
              height="400"
              viewBox="0 0 400 400"
            >
              {/* Concentric arcs */}
              {[1, 2, 3].map((i) => (
                <circle
                  key={i}
                  cx="200"
                  cy="200"
                  r={80 * i}
                  fill="none"
                  stroke="white"
                  strokeWidth="0.5"
                  opacity="0.2"
                />
              ))}

              {/* Crosshair */}
              <line x1="200" y1="50" x2="200" y2="350" stroke="white" strokeWidth="0.5" opacity="0.1" />
              <line x1="50" y1="200" x2="350" y2="200" stroke="white" strokeWidth="0.5" opacity="0.1" />
            </svg>

            {/* Data Points */}
            <div className="space-y-12">
              <motion.div variants={dataPointVariants} className="flex items-center gap-4">
                <span className="text-white text-2xl">●</span>
                <div>
                  <div className="text-white font-bold text-3xl">10+</div>
                  <div className="text-white opacity-60 text-xs uppercase tracking-wider" style={{ fontFamily: "'Space Mono', monospace" }}>
                    Years Experience
                  </div>
                </div>
              </motion.div>

              <motion.div variants={dataPointVariants} className="flex items-center gap-4">
                <span className="text-white text-2xl">●</span>
                <div>
                  <div className="text-white font-bold text-3xl">40+</div>
                  <div className="text-white opacity-60 text-xs uppercase tracking-wider" style={{ fontFamily: "'Space Mono', monospace" }}>
                    Workflows Built
                  </div>
                </div>
              </motion.div>

              <motion.div variants={dataPointVariants} className="flex items-center gap-4">
                <span className="text-white text-2xl">●</span>
                <div>
                  <div className="text-white font-bold text-3xl">95%</div>
                  <div className="text-white opacity-60 text-xs uppercase tracking-wider" style={{ fontFamily: "'Space Mono', monospace" }}>
                    Client Retention
                  </div>
                </div>
              </motion.div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
