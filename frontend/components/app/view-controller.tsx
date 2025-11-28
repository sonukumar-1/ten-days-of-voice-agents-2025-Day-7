'use client';

import { useRef } from 'react';
import { AnimatePresence, motion } from 'motion/react';
import { useRoomContext } from '@livekit/components-react';
import { useSession } from '@/components/app/session-provider';
import { SessionView } from '@/components/app/session-view';
import { WelcomeView } from '@/components/app/welcome-view';

/* eslint-disable @typescript-eslint/no-explicit-any */



const VIEW_MOTION_PROPS = {
  variants: {
    visible: {
      opacity: 1,
    },
    hidden: {
      opacity: 0,
    },
  },
  initial: 'hidden',
  animate: 'visible',
  exit: 'hidden',
  transition: {
    duration: 0.5,
    ease: 'linear',
  } as any,
};

export function ViewController() {
  const room = useRoomContext();
  const isSessionActiveRef = useRef(false);
  const { appConfig, isSessionActive, startSession } = useSession();


  // animation handler holds a reference to stale isSessionActive value
  isSessionActiveRef.current = isSessionActive;

  // disconnect room after animation completes
  const handleAnimationComplete = () => {
    if (!isSessionActiveRef.current && room.state !== 'disconnected') {
      room.disconnect();
    }
  };

  return (
    <AnimatePresence mode="wait">
      {/* Welcome screen */}
      {!isSessionActive && (
        <motion.div key="welcome" {...VIEW_MOTION_PROPS} className="absolute inset-0 z-10">
          <WelcomeView onStart={startSession} />
        </motion.div>
      )}
      {/* Session view */}
      {isSessionActive && (
        <motion.div
          key="session-view"
          {...(VIEW_MOTION_PROPS as any)}
          className="absolute inset-0 z-10"
          onAnimationComplete={handleAnimationComplete}
        >
          <SessionView
            appConfig={appConfig}
          />
        </motion.div>
      )}
    </AnimatePresence>
  );
}
