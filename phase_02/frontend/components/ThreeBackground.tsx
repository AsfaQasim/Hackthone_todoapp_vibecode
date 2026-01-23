'use client';

import { useEffect, useRef } from 'react';
import * as THREE from 'three';

const ThreeBackground = () => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Scene setup
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 5;

    // Renderer with transparent background
    const renderer = new THREE.WebGLRenderer({
      alpha: true,
      antialias: true,
      powerPreference: "high-performance"
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setClearColor(0x000000, 0); // Transparent background
    containerRef.current.appendChild(renderer.domElement);

    // Create floating particles with varying sizes and colors
    const particlesGeometry = new THREE.BufferGeometry();
    const particlesCount = 1500;

    const posArray = new Float32Array(particlesCount * 3);
    const velArray = new Float32Array(particlesCount * 3);
    const sizeArray = new Float32Array(particlesCount);
    const colorArray = new Float32Array(particlesCount * 3);

    // Color palette: soft blues and cyans
    const colors = [
      new THREE.Color('#22d3ee'), // cyan-400
      new THREE.Color('#06b6d4'), // cyan-500
      new THREE.Color('#0ea5e9'), // sky-500
      new THREE.Color('#3b82f6'), // blue-500
      new THREE.Color('#8b5cf6'), // violet-500
    ];

    for (let i = 0; i < particlesCount * 3; i += 3) {
      // Positions
      posArray[i] = (Math.random() - 0.5) * 20;
      posArray[i + 1] = (Math.random() - 0.5) * 20;
      posArray[i + 2] = (Math.random() - 0.5) * 20;

      // Velocities
      velArray[i] = (Math.random() - 0.5) * 0.005;
      velArray[i + 1] = (Math.random() - 0.5) * 0.005;
      velArray[i + 2] = (Math.random() - 0.5) * 0.005;

      // Random size for depth effect
      const idx = i / 3;
      sizeArray[idx] = Math.random() * 0.05 + 0.02;

      // Random color assignment
      const color = colors[Math.floor(Math.random() * colors.length)];
      colorArray[i] = color.r;
      colorArray[i + 1] = color.g;
      colorArray[i + 2] = color.b;
    }

    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    particlesGeometry.setAttribute('velocity', new THREE.BufferAttribute(velArray, 3));
    particlesGeometry.setAttribute('size', new THREE.BufferAttribute(sizeArray, 1));
    particlesGeometry.setAttribute('color', new THREE.BufferAttribute(colorArray, 3));

    // Particle material with custom shader for better visual effect
    const particlesMaterial = new THREE.ShaderMaterial({
      uniforms: {
        time: { value: 0 },
        pointSize: { value: 1.0 }
      },
      vertexShader: `
        attribute float size;
        attribute vec3 color;
        varying vec3 vColor;

        void main() {
          vColor = color;
          vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
          gl_PointSize = size * (300.0 / -mvPosition.z);
          gl_Position = projectionMatrix * mvPosition;
        }
      `,
      fragmentShader: `
        varying vec3 vColor;

        void main() {
          float distanceToCenter = distance(gl_PointCoord, vec2(0.5));

          if(distanceToCenter > 0.5) {
            discard;
          }

          float alpha = 1.0 - 2.0 * distanceToCenter;
          gl_FragColor = vec4(vColor, alpha * 0.7);
        }
      `,
      transparent: true,
      blending: THREE.AdditiveBlending,
    });

    const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particlesMesh);

    // Create floating abstract shapes (torus knots)
    const shapesGroup = new THREE.Group();
    const shapeCount = 8;

    for (let i = 0; i < shapeCount; i++) {
      const geometry = new THREE.TorusKnotGeometry(
        0.3 + Math.random() * 0.2, // radius
        0.1 + Math.random() * 0.05, // tube
        64, // tubularSegments
        16, // radialSegments
        2, // p
        3 // q
      );

      const material = new THREE.MeshBasicMaterial({
        color: new THREE.Color(
          0.2 + Math.random() * 0.3,
          0.6 + Math.random() * 0.3,
          0.8 + Math.random() * 0.2
        ),
        transparent: true,
        opacity: 0.1 + Math.random() * 0.15,
        wireframe: true
      });

      const shape = new THREE.Mesh(geometry, material);

      // Position randomly in 3D space
      shape.position.x = (Math.random() - 0.5) * 15;
      shape.position.y = (Math.random() - 0.5) * 15;
      shape.position.z = (Math.random() - 0.5) * 15;

      // Random rotation and scale
      shape.rotation.x = Math.random() * Math.PI;
      shape.rotation.y = Math.random() * Math.PI;
      const scale = 0.5 + Math.random() * 1.5;
      shape.scale.set(scale, scale, scale);

      // Store velocity for movement
      (shape as any).velocity = new THREE.Vector3(
        (Math.random() - 0.5) * 0.002,
        (Math.random() - 0.5) * 0.002,
        (Math.random() - 0.5) * 0.002
      );

      shapesGroup.add(shape);
    }

    scene.add(shapesGroup);

    // Animation loop
    let startTime = Date.now();
    const animate = () => {
      requestAnimationFrame(animate);

      const elapsedTime = (Date.now() - startTime) / 1000;

      // Update particles
      const positions = particlesGeometry.attributes.position.array as Float32Array;
      const velocities = particlesGeometry.attributes.velocity.array as Float32Array;

      for (let i = 0; i < particlesCount * 3; i += 3) {
        positions[i] += velocities[i];
        positions[i + 1] += velocities[i + 1];
        positions[i + 2] += velocities[i + 2];

        // Boundary checks to keep particles in view
        if (Math.abs(positions[i]) > 10) velocities[i] *= -1;
        if (Math.abs(positions[i + 1]) > 10) velocities[i + 1] *= -1;
        if (Math.abs(positions[i + 2]) > 10) velocities[i + 2] *= -1;
      }

      particlesGeometry.attributes.position.needsUpdate = true;

      // Update shapes
      shapesGroup.rotation.x = elapsedTime * 0.05;
      shapesGroup.rotation.y = elapsedTime * 0.03;

      shapesGroup.children.forEach(child => {
        child.rotation.x += 0.005;
        child.rotation.y += 0.003;

        // Move shapes slightly
        child.position.x += (child as any).velocity.x;
        child.position.y += (child as any).velocity.y;
        child.position.z += (child as any).velocity.z;

        // Boundary checks for shapes
        if (Math.abs(child.position.x) > 10) (child as any).velocity.x *= -1;
        if (Math.abs(child.position.y) > 10) (child as any).velocity.y *= -1;
        if (Math.abs(child.position.z) > 10) (child as any).velocity.z *= -1;
      });

      // Update shader time
      particlesMaterial.uniforms.time.value = elapsedTime;

      renderer.render(scene, camera);
    };

    // Handle resize
    const handleResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };

    window.addEventListener('resize', handleResize);
    animate();

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize);
      if (containerRef.current) {
        containerRef.current.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, []);

  return (
    <div
      ref={containerRef}
      className="fixed inset-0 z-0 pointer-events-none"
      style={{ background: 'linear-gradient(to bottom, #0f172a, #1e293b)' }}
    />
  );
};

export default ThreeBackground;