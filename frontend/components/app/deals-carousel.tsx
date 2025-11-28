'use client';

import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Tag, Crown } from '@phosphor-icons/react/dist/ssr';

interface Deal {
    id: string;
    name: string;
    price: number;
    description: string;
}

const DEALS: Deal[] = [
    {
        id: 'bk-014',
        name: 'Whopper Meal Deal',
        price: 299,
        description: '1 Veg or Chicken Whopper + 1 Medium Fries + 1 Pepsi.',
    },
    {
        id: 'bk-015',
        name: 'Family Feast',
        price: 599,
        description: '2 Whoppers + 2 Medium Fries + 2 Pepsis + 1 Onion Rings.',
    },
    {
        id: 'bk-016',
        name: 'Snack Box',
        price: 199,
        description: '1 Crispy Veg + 1 Small Fries + 1 Pepsi.',
    },
];

export function DealsCarousel() {
    const [currentIndex, setCurrentIndex] = useState(0);

    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentIndex((prev) => (prev + 1) % DEALS.length);
        }, 5000); // Rotate every 5 seconds
        return () => clearInterval(timer);
    }, []);

    return (
        <div className="relative w-full max-w-md overflow-hidden rounded-2xl border-2 border-[#502314]/20 bg-[#F5EBDC] shadow-xl">
            <div className="absolute top-0 left-0 z-10 flex items-center gap-1 rounded-br-xl bg-[#D62300] px-3 py-1 text-xs font-bold text-white uppercase tracking-wider">
                <Crown weight="fill" className="h-3 w-3 text-[#F5EBDC]" />
                King Deal
            </div>

            <div className="relative h-32 w-full p-4 pt-8">
                <AnimatePresence mode="wait">
                    <motion.div
                        key={currentIndex}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        transition={{ duration: 0.4 }}
                        className="flex h-full flex-col justify-between"
                    >
                        <div>
                            <h3 className="text-lg font-black text-[#502314] uppercase leading-tight">
                                {DEALS[currentIndex].name}
                            </h3>
                            <p className="mt-1 text-xs font-medium text-[#502314]/70 line-clamp-2">
                                {DEALS[currentIndex].description}
                            </p>
                        </div>
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-1 rounded-full bg-[#502314]/10 px-2 py-1">
                                <Tag className="h-3 w-3 text-[#D62300]" />
                                <span className="text-xs font-bold text-[#502314]">
                                    Limited Time
                                </span>
                            </div>
                            <span className="text-xl font-black text-[#D62300]">
                                ₹{DEALS[currentIndex].price}
                            </span>
                        </div>
                    </motion.div>
                </AnimatePresence>
            </div>

            {/* Progress Indicators */}
            <div className="absolute bottom-2 left-1/2 flex -translate-x-1/2 gap-1">
                {DEALS.map((_, idx) => (
                    <div
                        key={idx}
                        className={`h-1 rounded-full transition-all duration-300 ${idx === currentIndex ? 'w-4 bg-[#D62300]' : 'w-1 bg-[#502314]/20'
                            }`}
                    />
                ))}
            </div>
        </div>
    );
}
