"use client";

import { useEffect, useRef } from "react";

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  life: number;
  color: string;
  size: number;
}

interface KingdomParticlesProps {
  isActive: boolean;
  mode: "harmony" | "chaos";
}

export default function KingdomParticles({ isActive, mode }: KingdomParticlesProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !isActive) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Resize canvas to full screen
    const resizeObserver = new ResizeObserver(() => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    });
    resizeObserver.observe(canvas);
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles: Particle[] = [];
    const particleCount = mode === "harmony" ? 100 : 200; // More particles in chaos
    const colors = mode === "harmony" 
      ? ["#34D399", "#60A5FA", "#FBBF24"] // Emerald, Blue, Amber
      : ["#EF4444", "#7F1D1D", "#1F2937"]; // Red, Dark Red, Dark Gray

    // Initialize particles
    for (let i = 0; i < particleCount; i++) {
        particles.push(createParticle(canvas));
    }

    function createParticle(c: HTMLCanvasElement): Particle {
        return {
            x: Math.random() * c.width,
            y: Math.random() * c.height,
            vx: (Math.random() - 0.5) * (mode === "harmony" ? 0.5 : 2),
            vy: (Math.random() - 0.5) * (mode === "harmony" ? 0.5 : 2),
            life: Math.random() * 100,
            color: colors[Math.floor(Math.random() * colors.length)],
            size: Math.random() * 3 + 1
        };
    }

    const render = () => {
      // Clear with trail effect
      ctx.fillStyle = mode === "harmony" ? "rgba(26, 44, 42, 0.1)" : "rgba(20, 0, 0, 0.2)";
      ctx.fillRect(0, 0, canvas.width, canvas.height); // Trail effect
      
      // Update and draw particles
      particles.forEach((p, index) => {
        p.x += p.vx;
        p.y += p.vy;
        p.life -= 0.5;

        // Interaction with center (implied CORE at 50% 30% roughly)
        const coreX = canvas.width / 2;
        const coreY = canvas.height * 0.3; // Approx position of Castle

        if (mode === "harmony") {
            // Gentle orbit attraction
            const dx = coreX - p.x;
            const dy = coreY - p.y;
            const dist = Math.sqrt(dx*dx + dy*dy);
            p.vx += (dx / dist) * 0.02; // Pull to center
            p.vy += (dy / dist) * 0.02;
        } else {
            // Chaos repulsion / jitter
             p.vx += (Math.random() - 0.5) * 0.5;
             p.vy += (Math.random() - 0.5) * 0.5;
        }

        // Draw
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.life / 100;
        ctx.fill();
        ctx.globalAlpha = 1.0;

        // Reset dead or out of bound particles
        if (p.life <= 0 || p.x < 0 || p.x > canvas.width || p.y < 0 || p.y > canvas.height) {
            particles[index] = createParticle(canvas);
        }
      });

      animationRef.current = requestAnimationFrame(render);
    };

    render();

    return () => {
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
      resizeObserver.disconnect();
    };
  }, [isActive, mode]);

  // If not active, return null (or transparent div)
  if (!isActive) return null;

  return (
    <canvas 
        ref={canvasRef} 
        className="absolute inset-0 pointer-events-none z-10 mix-blend-screen"
    />
  );
}
