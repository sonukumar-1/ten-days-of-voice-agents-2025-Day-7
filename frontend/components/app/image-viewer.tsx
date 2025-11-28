'use client';

import { useEffect, useState } from 'react';
import { AnimatePresence, motion } from 'motion/react';
import { X } from '@phosphor-icons/react';

interface ImageViewerProps {
  imageUrl: string | null;
  prompt: string | null;
  onClose: () => void;
}

export function ImageViewer({ imageUrl, prompt, onClose }: ImageViewerProps) {
  return (
    <AnimatePresence>
      {imageUrl && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 p-4 backdrop-blur-sm"
          onClick={onClose}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="bg-card relative w-full max-w-3xl overflow-hidden rounded-2xl border border-white/10 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              onClick={onClose}
              className="absolute top-4 right-4 z-10 rounded-full bg-black/50 p-2 text-white backdrop-blur-md transition-colors hover:bg-black/70"
            >
              <X size={20} weight="bold" />
            </button>

            <div className="relative aspect-square w-full bg-black/20 md:aspect-video">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={imageUrl}
                alt={prompt || 'Generated Image'}
                className="h-full w-full object-contain"
              />
            </div>

            {prompt && (
              <div className="bg-card border-border border-t p-4">
                <p className="text-muted-foreground mb-1 text-sm font-medium tracking-wider uppercase">
                  Generated from prompt
                </p>
                <p className="text-foreground font-medium">{prompt}</p>
              </div>
            )}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
