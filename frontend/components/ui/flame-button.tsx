'use client';

import React from 'react';
import { motion, HTMLMotionProps } from 'motion/react';
import { ArrowRight } from '@phosphor-icons/react/dist/ssr';
import { cn } from '@/lib/utils';

interface FlameButtonProps extends HTMLMotionProps<'button'> {
    onClick?: () => void;
    className?: string;
}

export function FlameButton({ onClick, className, ...props }: FlameButtonProps) {
    return (
        <div className="relative group">
            {/* Outer Glow - Pulsing */}
            <motion.div
                animate={{
                    scale: [1, 1.05, 1],
                    opacity: [0.5, 0.8, 0.5],
                }}
                transition={{
                    duration: 2,
                    repeat: Infinity,
                    ease: "easeInOut",
                }}
                className="absolute inset-0 rounded-full bg-[#D62300] blur-xl"
            />

            {/* Inner Glow - Intense */}
            <motion.div
                animate={{
                    scale: [1, 1.02, 1],
                    opacity: [0.8, 1, 0.8],
                }}
                transition={{
                    duration: 1.5,
                    repeat: Infinity,
                    ease: "easeInOut",
                    delay: 0.2,
                }}
                className="absolute inset-1 rounded-full bg-[#E55F25] blur-md"
            />

            {/* Button Itself */}
            <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={onClick}
                className={cn(
                    "relative flex items-center gap-3 overflow-hidden rounded-full bg-gradient-to-r from-[#D62300] via-[#E55F25] to-[#D62300] bg-[length:200%_100%] px-10 py-8 text-lg font-bold text-white shadow-2xl ring-4 ring-[#D62300]/30",
                    className
                )}
                {...props}
            >
                {/* Shimmer Effect */}
                <motion.div
                    animate={{
                        backgroundPosition: ["200% 0", "-200% 0"],
                    }}
                    transition={{
                        duration: 3,
                        repeat: Infinity,
                        ease: "linear",
                    }}
                    className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent bg-[length:200%_100%]"
                    style={{ backgroundSize: "200% 100%" }}
                />

                <span className="relative z-10">Start Ordering</span>
                <ArrowRight className="relative z-10 h-5 w-5 transition-transform group-hover:translate-x-1" />
            </motion.button>
        </div>
    );
}
