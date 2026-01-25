'use client';

import React, { useEffect, useRef } from 'react';

// Define particle types
type ParticleType = 'sphere' | 'cube' | 'star';

class Particle {
  x: number;
  y: number;
  z: number;
  originalX: number;
  originalY: number;
  size: number;
  speed: number;
  baseSize: number;
  type: ParticleType;
  rotation: number;
  rotationSpeed: number;
  angle: number; // For spiral positioning
  distance: number; // Distance from center for spiral formation
  armOffset: number; // Offset for spiral arm positioning

  constructor(width: number, height: number) {
    // Position particles in a spiral galaxy formation
    const centerX = width / 2;
    const centerY = height / 2;

    // Create spiral arm pattern
    this.armOffset = Math.random() * Math.PI * 2;
    this.angle = Math.random() * Math.PI * 2;
    this.distance = Math.sqrt(Math.random()) * Math.min(width, height) * 0.4;

    // Calculate position based on spiral formula
    const spiralFactor = 0.2;
    const spiralTurns = 3;
    const adjustedAngle = this.angle + this.armOffset + spiralFactor * this.distance * spiralTurns;

    this.originalX = centerX + Math.cos(adjustedAngle) * this.distance;
    this.originalY = centerY + Math.sin(adjustedAngle) * this.distance;

    this.x = this.originalX;
    this.y = this.originalY;
    this.z = Math.random() * 1000; // Z coordinate for depth
    this.size = Math.random() * 2 + 0.5;
    this.baseSize = this.size;
    this.speed = Math.random() * 0.2 + 0.05; // Slower movement for galaxy feel
    this.type = this.determineParticleType(); // Randomly assign particle type
    this.rotation = Math.random() * Math.PI * 2;
    this.rotationSpeed = (Math.random() - 0.5) * 0.02; // Slower rotation
  }

  determineParticleType(): ParticleType {
    const rand = Math.random();
    if (rand < 0.7) return 'sphere'; // 70% spheres (stars)
    if (rand < 0.9) return 'star'; // 20% stars
    return 'cube'; // 10% cubes (cosmic dust/asteroids)
  }

  update(mouseX: number, mouseY: number) {
    // Move particles based on mouse position for parallax effect
    const dx = mouseX - this.originalX;
    const dy = mouseY - this.originalY;

    // Depth calculation - particles closer to viewer appear larger and faster
    const perspective = 500 / (500 + this.z);
    this.x = this.originalX + dx * 0.0002 * perspective; // Reduced parallax effect for galaxy feel
    this.y = this.originalY + dy * 0.0002 * perspective;

    // Move particles toward the viewer to create depth illusion
    this.z -= this.speed;

    // Reset particles that come too close to the viewer
    if (this.z <= 0) {
      this.z = 1000;
      // Reset to a new position in the spiral
      const centerX = window.innerWidth / 2;
      const centerY = window.innerHeight / 2;

      this.armOffset = Math.random() * Math.PI * 2;
      this.angle = Math.random() * Math.PI * 2;
      this.distance = Math.sqrt(Math.random()) * Math.min(window.innerWidth, window.innerHeight) * 0.4;

      const spiralFactor = 0.2;
      const spiralTurns = 3;
      const adjustedAngle = this.angle + this.armOffset + spiralFactor * this.distance * spiralTurns;

      this.originalX = centerX + Math.cos(adjustedAngle) * this.distance;
      this.originalY = centerY + Math.sin(adjustedAngle) * this.distance;
      this.x = this.originalX;
      this.y = this.originalY;
    }

    // Update size based on depth
    this.size = this.baseSize * perspective;

    // Update rotation
    this.rotation += this.rotationSpeed;
  }

  draw(ctx: CanvasRenderingContext2D) {
    const alpha = 1 - (this.z / 1000); // Fade out distant particles

    if (this.type === 'sphere') {
      // Draw spherical particle (star)
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      // Use varying colors for stars
      const hue = 200 + Math.random() * 40; // Blue/cyan range
      ctx.fillStyle = `hsla(${hue}, 80%, 70%, ${alpha * 0.8})`;
      ctx.fill();

      // Add glow effect
      const gradient = ctx.createRadialGradient(
        this.x, this.y, 0,
        this.x, this.y, this.size * 3
      );
      gradient.addColorStop(0, `hsla(${hue}, 100%, 80%, ${alpha * 0.6})`);
      gradient.addColorStop(1, `hsla(${hue}, 100%, 50%, 0)`);

      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size * 3, 0, Math.PI * 2);
      ctx.fillStyle = gradient;
      ctx.fill();
    }
    else if (this.type === 'star') {
      // Draw star-shaped particle
      ctx.save();
      ctx.translate(this.x, this.y);
      ctx.rotate(this.rotation);

      const points = 5;
      const outerRadius = this.size * 2;
      const innerRadius = this.size;

      ctx.beginPath();
      for (let i = 0; i < points * 2; i++) {
        const radius = i % 2 === 0 ? outerRadius : innerRadius;
        const angle = (Math.PI / points) * i - Math.PI / 2;
        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;

        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }
      ctx.closePath();

      // Use yellow/white colors for stars
      const hue = 50 + Math.random() * 20; // Yellow/white range
      ctx.fillStyle = `hsla(${hue}, 100%, 80%, ${alpha * 0.9})`;
      ctx.fill();

      // Add glow effect
      const gradient = ctx.createRadialGradient(
        0, 0, 0,
        0, 0, outerRadius * 2
      );
      gradient.addColorStop(0, `hsla(${hue}, 100%, 90%, ${alpha * 0.7})`);
      gradient.addColorStop(1, `hsla(${hue}, 100%, 50%, 0)`);

      ctx.beginPath();
      for (let i = 0; i < points * 2; i++) {
        const radius = i % 2 === 0 ? outerRadius * 1.5 : innerRadius * 1.5;
        const angle = (Math.PI / points) * i - Math.PI / 2;
        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;

        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }
      ctx.closePath();
      ctx.fillStyle = gradient;
      ctx.fill();

      ctx.restore();
    }
    else {
      // Draw cube particle with rotation (cosmic dust/asteroids)
      ctx.save();
      ctx.translate(this.x, this.y);
      ctx.rotate(this.rotation);

      // Draw a cube-like shape (rotated square with depth effect)
      const halfSize = this.size;
      // Use brown/orange colors for cosmic dust
      const hue = 30 + Math.random() * 30; // Brown/orange range
      ctx.fillStyle = `hsla(${hue}, 70%, 60%, ${alpha * 0.7})`;

      // Draw the main face of the cube
      ctx.fillRect(-halfSize, -halfSize, halfSize * 2, halfSize * 2);

      // Draw a highlight to simulate 3D effect
      ctx.fillStyle = `hsla(${hue + 20}, 80%, 70%, ${alpha * 0.5})`;
      ctx.fillRect(-halfSize * 0.7, -halfSize * 0.7, halfSize * 1.4, halfSize * 0.5);

      ctx.restore();
    }
  }
}

const ThreeDBackground = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size to match window
    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // Galaxy particles configuration
    const particles: Particle[] = [];
    const totalParticles = 300; // More particles for galaxy density
    let mouseX = canvas.width / 2;
    let mouseY = canvas.height / 2;

    // Track mouse position
    const handleMouseMove = (e: MouseEvent) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    };

    window.addEventListener('mousemove', handleMouseMove);

    // Initialize particles in spiral formation
    for (let i = 0; i < totalParticles; i++) {
      particles.push(new Particle(canvas.width, canvas.height));
    }

    // Animation loop
    const animate = () => {
      if (!ctx) return;

      // Dark space background with slight fade for trails
      ctx.fillStyle = 'rgba(10, 10, 30, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Update and draw particles
      particles.forEach(particle => {
        particle.update(mouseX, mouseY);
        particle.draw(ctx);
      });

      requestAnimationFrame(animate);
    };

    animate();

    // Cleanup
    return () => {
      window.removeEventListener('resize', resizeCanvas);
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed top-0 left-0 w-full h-full -z-50"
      style={{ background: 'radial-gradient(ellipse at center, #0a0a1e 0%, #000000 100%)' }}
    />
  );
};

export default ThreeDBackground;